from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.template.defaulttags import register
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import re
from django.core.mail import send_mail, EmailMessage
from ta_logistics_application.forms import StudentProfileForm, CreateClassForm, OptionalFieldsForm, ApplicationForm, AddOptionalFieldForm
from ta_logistics_application.models import Classes, ClassApplicants, DataDefinitions, Students, ApplicationFields


# CONSTANTS GO HERE
APP_SUBMITTED = 0
APP_PENDING = 1
APP_COMPLETE = 2

HIRE_REVIEW = 0
HIRE_REJECT = 1
HIRE_INTERVIEW = 2
HIRE_ACCEPT = 3
HIRE_WAIT = 4


def login(request):
    template = loader.get_template('ta_logistics_application/login.html')
    return HttpResponse(template.render())


@login_required(login_url='login')
def group_index(request):
    if request.user.is_authenticated():
        if request.user.groups.all()[0].name == "faculty":
            return render(request, 'ta_logistics_application/professor/professor_index.html')
        elif request.user.groups.all()[0].name == "student":
            template = loader.get_template('ta_logistics_application/student/profile.html')
            return HttpResponse(template.render())


################ Student Context ################


def student_profile(request):
    # This view will be shown to students the first time they login to the app
    # or if you then want to edit any information in their profile.
    #Will eventually retrieve data to show which student has applied to what class

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            template = loader.get_template('ta_logistics_application/student/submission_received.html')
            return HttpResponse(template.render())
    else:
        form = StudentProfileForm()
    return render(request, 'ta_logistics_application/student/profile.html', {'form': form})


def student_status(request):
    # This view will retrieve the classes that the current student applied to

    applied_classes = Status.objects.filter(ubit_name='fgpinnoc')
    context = {'applied_classes': applied_classes}
    return render(request, 'ta_logistics_application/student/status.html', context)



def student_class_list(request):
    #This view will retrive all the possible classes offered to TA

    return render(request, 'ta_logistics_application/student/class_list.html')

# Finish when student index is finished
# Get s_id and c_id parts working
def student_application(request, class_id=None):#, c_id, s_id):
    c_id = 13
    s_id = 1
    if request.method == 'POST':
        form = ApplicationForm(request.POST, class_id=c_id, student_id=s_id)
        if form.is_valid():
            form.save()
            template = loader.get_template('ta_logistics_application/student/submission_received.html')
            return HttpResponse(template.render())

    form = ApplicationForm(class_id=c_id, student_id=s_id)
    return render(request, 'ta_logistics_application/student/application.html', {'form': form})

################ Professor Context ################
@login_required(login_url='login')
def professor_index(request):
    p_id = 1
    current_class_list = Classes.objects.filter(professor_id=p_id, is_active=True).values()
    for current_class in current_class_list:
        current_class['applicant_count'] = ClassApplicants.objects.filter(class_id=current_class['id']).count()
    context = {
        'current_class_list' : current_class_list
    }
    template = loader.get_template('ta_logistics_application/professor/professor_index.html')
    return render(request, 'ta_logistics_application/professor/professor_index.html', context)


@login_required(login_url='login')
def professor_create_class(request):
    if request.method == 'POST':
        selected_optionals = request.POST.getlist("select_optional_fields")
        # Hacky solution, possible rework in the future
        request.POST['selected_optional_field_ids'] = ','.join(map(str,selected_optionals))
        # Replace this with ID of professor that is signed in
        request.POST['professor_id'] = 1
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
def professor_class_applicants(request):
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
                if 'interview' in request_list:
                    application_entry.application_status_id = APP_PENDING
                    application_entry.hiring_status_id = HIRE_INTERVIEW
                    subject = "You've been selected for an interview!"
                    body = "You've been selected for an interview!"
                elif 'hired' in request_list:
                    application_entry.application_status_id = APP_COMPLETE
                    application_entry.hiring_status_id = HIRE_ACCEPT
                    subject = "Congratulations, You've been Hired!"
                    body = "Congratulations, You've been Hired!"
                elif 'wait_listed' in request_list:
                    application_entry.application_status_id = APP_PENDING
                    application_entry.hiring_status_id = HIRE_WAIT
                    subject = "Application Pending"
                    body = "Application Pending"
                elif 'reject' in request_list:
                    application_entry.application_status_id = APP_COMPLETE
                    application_entry.hiring_status_id = HIRE_REJECT
                    subject = "Sorry"
                    body = "Sorry"
                else:
                    break
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

                if not ubit_name in error_students:
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
def view_optional_fields(request):
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
def edit_optional_field(request):
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
def add_optional_field(request):
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
