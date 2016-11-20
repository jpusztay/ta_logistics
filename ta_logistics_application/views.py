from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.template.defaulttags import register
from django.template import loader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
import re
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.core.mail import send_mail, EmailMessage
from ta_logistics_application.forms import StudentProfileForm, CreateClassForm, OptionalFieldsForm, ApplicationForm, AddOptionalFieldForm, ClassListForm, ProfessorProfileForm
from ta_logistics_application.models import Classes, ClassApplicants, DataDefinitions, Students, ApplicationFields, Professors
import ta_logistics_application.models
from django.contrib.auth.views import login


HIRE_REVIEW = 0
HIRE_REJECT = 1
HIRE_INTERVIEW = 2
HIRE_OFFERED = 3
HIRE_WAIT = 4
HIRE_ACCEPT = 5
HIRE_DECLINE = 6


## Auth Stuff
def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home/")
    else:
        return login(request)


def check_faculty(user):
    return user.groups.filter(name="professors").exists()


def check_student(user):
    return user.groups.filter(name="students").exists()


@login_required(login_url='login')
def group_index(request):
    if request.user.is_authenticated():
        print(str(request.user.id))
        if request.user.is_staff:
            return HttpResponseRedirect("/admin/")
        if not request.user.groups.filter(name="professors").exists():
            request.user.groups.set([1])
        if request.user.groups.filter(name="professors").exists():
            if not Professors.objects.filter(pk=request.user.id).exists():
                return professor_profile(request)
            return professor_index(request)
        elif request.user.groups.filter(name="students").exists():
            if Students.objects.filter(pk=request.user.id).exists():
                return student_index(request)
            else:
                return student_profile(request)


################ Student Context ################

@login_required()
#@user_passes_test(check_student)
def student_index(request):
    """
    This view will display the list of classes that the student has applied to TA from the "status"
    table.
    :param request:
    :return:
    """
    if not check_student(request.user):
        raise PermissionDenied
    if request.method == "POST":
        print(request.POST)
        accept_offer = "accept" in request.POST;
        for key, val in request.POST.items():
            if key.startswith("class_"):
                curr_class = ClassApplicants.objects.get(student_id=request.user.id, class_id=key.split('_')[-1])
                curr_class.pending_offer = False
                if accept_offer:
                    curr_class.hiring_status_id = HIRE_ACCEPT
                else:
                    curr_class.hiring_status_id = HIRE_DECLINE
                curr_class.save()
    data_defs = DataDefinitions()
    applied_classes = data_defs.getStudentAppliedClasses(student_id=request.user.id)
    pending_offer = False
    for classes in applied_classes:
        if classes['pending_offer']:
            pending_offer = True
    context = {
        'applied_classes': applied_classes,
        'pending_offer': pending_offer
    }
    return render(request, 'ta_logistics_application/student/student_index.html', context)


@login_required()
#@user_passes_test(check_student)
def student_profile(request):
    """
    This view will be shown to students the first time they login to the app or if you then want to
    edit any information in their profile.
    :param request:
    :return:
    """
    if not check_student(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        request.POST['id'] = request.user.id
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            template = loader.get_template('ta_logistics_application/student/submission_received.html')
            return HttpResponse(template.render())
    else:
        form = StudentProfileForm()
    return render(request, 'ta_logistics_application/student/profile.html', {'form': form})


@login_required()
#@user_passes_test(check_student)
def student_class_list(request):
    """
    This view will display a dropdown list of classes that students can apply to TA.
    :param request:
    :return:
    """
    if not check_student(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        class_id = request.POST['selected_class']
        return redirect('/student/application?class_id='+str(class_id))

    class_list = Classes.objects.filter(is_active=True).values('id', 'class_listing_id', 'class_name').order_by('class_listing_id')
    context = {
        'class_list': class_list,
    }
    return render(request, 'ta_logistics_application/student/class_list.html', context)


# Get s_id and c_id parts working
@login_required()
#@user_passes_test(check_student)
def student_application(request):# s_id):
    if not check_student(request.user):
        raise PermissionDenied
    class_id = int(request.GET.urlencode().split('=')[-1])
    s_id = request.user.id
    if request.method == 'POST':
        form = ApplicationForm(request.POST, class_id=class_id, student_id=s_id)
        if form.is_valid():
            form.save()
            template = loader.get_template('ta_logistics_application/student/submission_received.html')
            return HttpResponse(template.render())
    selected_class = Classes.objects.get(id=class_id).class_listing_id
    form = ApplicationForm(class_id=class_id, student_id=s_id)
    context = {
        'selected_class': selected_class,
        'form': form
    }
    return render(request, 'ta_logistics_application/student/application.html', context)


################ Professor Context ################

@login_required()
#@user_passes_test(check_student)
def professor_profile(request):
    """
    This view will be shown to professors the first time they login to the app or if you then want to
    edit any information in their profile.
    :param request:
    :return:
    """
    if not check_faculty(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        request.POST['id'] = request.user.id
        print(request.POST)
        form = ProfessorProfileForm(request.POST)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect("/home")
    else:
        form = ProfessorProfileForm()
    return render(request, 'ta_logistics_application/professor/professor_information.html', {'form': form})


@login_required(login_url='login')
#@user_passes_test(check_faculty)
def professor_index(request):
    if not check_faculty(request.user):
        raise PermissionDenied
    p_id = request.user.id
    if request.method == "POST":
        print(request.POST)
        is_active = "set_active" in request.POST;
        for key, val in request.POST.items():
            if key.startswith("class_"):
                curr_class = Classes.objects.get(id=key.split('_')[-1])
                curr_class.is_active = is_active
                curr_class.save()
    current_class_list = Classes.objects.filter(professor_id=p_id).values()
    for current_class in current_class_list:
        current_class['applicant_count'] = ClassApplicants.objects.filter(class_id=current_class['id']).count()
    context = {
        'current_class_list' : current_class_list
    }
    return render(request, 'ta_logistics_application/professor/professor_index.html', context)


@login_required(login_url='login')
#@user_passes_test(check_faculty)
def professor_create_class(request):
    if not check_faculty(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        selected_optionals = request.POST.getlist("select_optional_fields")
        # Hacky solution, possible rework in the future
        request.POST['selected_optional_field_ids'] = ','.join(map(str,selected_optionals))
        # Replace this with ID of professor that is signed in
        request.POST['professor_id'] = request.user.id
        form = CreateClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(professor_index)
        else:
            print(form.errors)
            return redirect(professor_index)

    context = {
        'form': CreateClassForm(),
        'optional_fields': OptionalFieldsForm()
    }
    return render(request, 'ta_logistics_application/professor/create_class.html', context)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key).items()


@login_required(login_url='login')
#@user_passes_test(check_faculty)
def professor_class_applicants(request):
    if not check_faculty(request.user):
        raise PermissionDenied

    class_id = int(request.GET.urlencode().split('=')[-1])
    if request.method == 'POST':
        error_students = []
        students = []
        for key, val in request.POST.items():
            if key.startswith("ubit"):
                ubit_name = key.split("_")[-1]
                email_address = ubit_name + '@buffalo.edu'
                student_id = Students.objects.get(ubit_name=ubit_name).id
                application_entry = ClassApplicants.objects.get(student_id=student_id, class_id=class_id)
                request_list = list(request.POST.keys())
                send_email = True
                if 'interview' in request_list:
                    application_entry.hiring_status_id = HIRE_INTERVIEW
                    subject = "You've been selected for an interview!"
                    body = "You've been selected for an interview!"
                elif 'hired' in request_list:
                    application_entry.hiring_status_id = HIRE_OFFERED
                    application_entry.pending_offer = True
                    subject = "Congratulations, You've been given an offer!"
                    body = "Congratulations, You've been given an offer!"
                elif 'wait_listed' in request_list:
                    application_entry.hiring_status_id = HIRE_WAIT
                    send_email = False
                elif 'reject' in request_list:
                    application_entry.hiring_status_id = HIRE_REJECT
                    subject = "Sorry"
                    body = "Sorry"
                else:
                    break

                if send_email:
                    email_message = EmailMessage(
                        subject,
                        body,
                        'cse442.talogistics@gmail.com',
                        [email_address],
                    )
                    try:
                        email_message.send(fail_silently=False)
                    except:
                        # Return error-sending-email page, status not changed
                        error_students.append(ubit_name)

                if ubit_name not in error_students:
                    students.append(ubit_name)
                application_entry.save()
        context = {
            'students': students,
            'error_students': error_students,
        }
        return render(request, 'ta_logistics_application/professor/professor_email_sent.html', context)

    data_defs = DataDefinitions()
    main_student_data = data_defs.getStudentDataForApplicantsView(class_id=class_id)
    if main_student_data:
        num_cols = len(main_student_data[0])
    else:
        num_cols = 0
    context = {
        'main_student_data': main_student_data,
        'num_cols': num_cols,
    }

    return render(request, 'ta_logistics_application/professor/professor_class_applicants.html', context)


@login_required(login_url='login')
#@user_passes_test(check_faculty)
def view_optional_fields(request):
    if not check_faculty(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        request_list = list(request.POST.keys())
        if 'edit' in request_list:
            field_id = -1
            for key, val in request.POST.items():
                if key.startswith('id_'):
                    field_id = key.split('_')[-1]
                    return redirect('edit_optional_field.html?field_id=' + field_id)
        elif 'create' in request_list:
            return redirect('add_optional_field.html')
    fields = ApplicationFields.objects.filter(is_default=False)
    context = {
        'fields': fields,
    }
    return render(request, 'ta_logistics_application/professor/view_optional_fields.html', context)


@login_required(login_url='login')
#@user_passes_test(check_faculty)
def edit_optional_field(request):
    if not check_faculty(request.user):
        raise PermissionDenied

    field_id = int(request.GET.urlencode().split('=')[-1])
    if request.method == 'POST':
        post = request.POST.copy()
        field_text = post.get('field_text')
        max_length = post.get('max_length')
        select_options_str = post.get('select_options')
        select_options = select_options_str.split('\r\n')
        for opts in select_options:
            opts = re.sub(' +', ' ', opts)
        field = ApplicationFields.objects.get(id=field_id)
        field.field_text = field_text
        field.max_length = max_length
        field.select_options = ','.join(select_options)
        field.save()
        return redirect('view_optional_fields.html')
    field = dict(ApplicationFields.objects.get(id=field_id).__dict__)
    select_options_str = field['select_options']
    select_options = select_options_str.split(',')
    field['select_options'] = '\r\n'.join(select_options)
    form = AddOptionalFieldForm(initial=field)
    return render(request, 'ta_logistics_application/professor/edit_optional_field.html', {'form': form})


@login_required(login_url='login')
#@user_passes_test(check_faculty)
def add_optional_field(request):
    if not check_faculty(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        post = request.POST.copy()
        field_text = post.get('field_text')
        select_options_str = post.get('select_options')
        select_options = select_options_str.split('\r\n')
        for opts in select_options:
            opts = re.sub(' +', ' ', opts)
        mutable = post._mutable
        post._mutable = True
        post['select_options'] = ','.join(select_options)
        post['field_name'] = re.sub('[^A-Za-z0-9]+', '', field_text)
        post._mutable = mutable
        print(post)
        form = AddOptionalFieldForm(post)
        if form.is_valid():
            # file is saved
            form.save()
            return redirect('view_optional_fields.html')
        else:
            print(form.errors)

    form = AddOptionalFieldForm()
    return render(request, 'ta_logistics_application/professor/add_optional_field.html', {'form': form})
