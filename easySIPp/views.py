from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.core.management import call_command
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from .forms import UACForm, UASForm
from .forms import xmlUploadForm
from .models import UacAppConfig, UasAppConfig
from .scripts.ksipp import get_sipp_processes, clean_filename, run_uac, run_uas, delete_old_screen_logs
from .scripts.list import list_xml_files
import xml.etree.ElementTree as ET
import psutil
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

################### Index Page Functions #############################

@never_cache
def index(request):
    showMoreOptionsForm = False
    uac_form = None
    uas_form = None
    uac_choices = list(UacAppConfig.objects.values_list('uac_key', 'uac_config_name'))
    uas_choices = list(UasAppConfig.objects.values_list('uas_key', 'uas_config_name'))

    # If database is empty, load initial data automatically
    if not uac_choices or not uas_choices:
        try:
            call_command('load_initial_if_empty')
            messages.success(request, 'Initial data loaded successfully!')
            # Refresh the choices after loading
            uac_choices = list(UacAppConfig.objects.values_list('uac_key', 'uac_config_name'))
            uas_choices = list(UasAppConfig.objects.values_list('uas_key', 'uas_config_name'))
        except Exception as e:
            messages.error(request, f'Error loading initial data: {str(e)}')
            return render(request, 'index.html', {})

    if request.method == 'POST':
        if 'selected_key' in request.POST:
            selected_key = request.POST['selected_key']

            if selected_key.startswith('uac'):
                uac_config = UacAppConfig.objects.get(uac_key=selected_key)
                uac_config.is_active_config = True
                uac_config.save()

            elif selected_key.startswith('uas'):
                uas_config = UasAppConfig.objects.get(uas_key=selected_key)
                uas_config.is_active_config = True
                uas_config.save()
            
            return redirect('index')


        elif 'save_conf' in request.POST:
            save_conf = request.POST['save_conf']

            if save_conf in ['save_uac', 'save_run_uac']:
                selected_uac_key = request.POST.get('uac_key')
                if selected_uac_key:
                    uac_config = UacAppConfig.objects.get(uac_key=selected_uac_key)
                    uac_form = UACForm(request.POST, instance=uac_config, uac_choices=uac_choices)

                    if uac_form.is_valid():
                        uac_form.save()
                        if save_conf == 'save_run_uac':
                            sipp_error = run_uac(uac_config)
                            if sipp_error:
                                messages.error(request, sipp_error)
                        
                        return redirect('index')

                    else:
                        logger.warning(uac_form.errors)
                        fields_to_check = ['called_party_number', 'calling_party_number', 'stun_server',
                                           'total_no_of_calls', 'cps']
                        showMoreOptionsForm = any(field in uac_form.errors for field in fields_to_check)


            elif save_conf in ['save_uas', 'save_run_uas']:
                selected_uas_key = request.POST.get('uas_key')
                if selected_uas_key:
                    uas_config = UasAppConfig.objects.get(uas_key=selected_uas_key)
                    uas_form = UASForm(request.POST, instance=uas_config, uas_choices=uas_choices)      
                    if uas_form.is_valid():
                        uas_form.save()                        
                        if save_conf == 'save_run_uas':
                            sipp_error = run_uas(uas_config)
                            if sipp_error:
                                messages.error(request, sipp_error)
                        
                        return redirect('index')
                    else:
                        logger.warning(uas_form.errors)


        elif 'send_signal' in request.POST:
            send_signal = request.POST.get('send_signal')
            pid = request.POST.get('pid_to_kill')

            if send_signal == 'Kill':
                try:
                    process = psutil.Process(int(pid))
                    process.terminate()  # can use process.kill() for a more forceful termination
                    process.wait(timeout=2)  # Wait for it to exit
                except (psutil.NoSuchProcess, psutil.TimeoutExpired) as e:
                    logger.exception(e)
                    pass
            
            elif send_signal == 'CheckOutput':
                try:
                    script_name = request.POST.get('script_name')
                    xml_wo_ext = script_name.rsplit(".", 1)[0]

                    cport = request.POST.get('cport')
                    mcalls = request.POST.get('mcalls')
                    process = psutil.Process(int(pid))
                    return redirect(f'{reverse("display_sipp_screen", kwargs={"xml": xml_wo_ext, "pid": process.pid})}?cp={cport}&m={mcalls}')

                
                except (psutil.NoSuchProcess, ProcessLookupError):
                    return redirect('display_sipp_screen', xml=xml_wo_ext, pid=pid)


    # To make sure to form was not already loaded and avoid refreshing despite form errors
    if not uac_form:
        uac_config = UacAppConfig.objects.get(is_active_config=True)
        uac_form = UACForm(instance=uac_config, uac_choices = uac_choices)
    if not uas_form:
        uas_config = UasAppConfig.objects.get(is_active_config=True)
        uas_form = UASForm(instance=uas_config, uas_choices=uas_choices)

    uac_xml = uac_config.select_uac
    uas_xml = uas_config.select_uas

    print_uac_command = f""
    print_uas_command = f""

    sipp_processes = get_sipp_processes()
    context = {
        'uac_xml': uac_xml,
        'uas_xml': uas_xml,
        'print_uac_command': print_uac_command,
        'print_uas_command': print_uas_command,
        'UACForm': uac_form,
        'UASForm': uas_form,
        'sipp_processes': sipp_processes,
        'showMoreOptionsForm': showMoreOptionsForm if 'showMoreOptionsForm' in locals() else False,
        'sipp_error': sipp_error if 'sipp_error' in locals() else False
        }

    return render(request, 'index.html', context)

######## Index End ############


def serve_xml_file(request, xmlname):
    xml_path = Path(settings.BASE_DIR) / 'easySIPp' / 'xml' / xmlname
    with open(xml_path, 'r') as file:
        xmlContent = file.read()
    return HttpResponse(xmlContent, content_type='text/plain')


def xml_editor(request):
    xml_path = Path(settings.BASE_DIR) / 'easySIPp' / 'xml'
    if request.method == 'GET':
        xmlName=request.GET.get('xml')
        referer=request.GET.get('back', 'index')
        if xmlName is None:
            return HttpResponse('No xml selected <a href="/xml-management/">Select here!</a>')

        with open(xml_path / xmlName, 'r', encoding='utf-8') as file:
            xmlContent = file.read()

    if request.method == 'POST':
        xmlContent = request.POST.get('xml_content')
        xmlName = request.POST.get('xml_name')
        new_xml_name = request.POST.get('new_xml_name')
        save_type = request.POST.get('save')
        referer = request.POST.get('exit')
        # Replace double line breaks with single line breaks
        xmlContent = xmlContent.replace('\r\n', '\n')

        if save_type == 'save': savingXmlName = xmlName
        elif save_type == 'save_as': 
            uacuas = 'uac' if xmlName.startswith('uac') else ('uas' if xmlName.startswith('uas') else None)
            savingXmlName = f'{uacuas}_{new_xml_name}.xml'
            savingXmlName = clean_filename(savingXmlName)
        else:  return redirect(referer)
        
        # if file name already exists, do not overwrite, show error
        if save_type == 'save_as' and (xml_path / savingXmlName).exists():
            error_msg = f"File '{savingXmlName}' already exists. Choose a different name."
            save_type = False
        
        else:
            with open(xml_path / savingXmlName, 'w', encoding='utf-8') as file:
                file.write(xmlContent)

            xmlName = savingXmlName

    
    context = {
        'xml_content':xmlContent,
        'xml_name':xmlName,
        'save': save_type if 'save_type' in locals() else False,
        'error_msg': error_msg if 'error_msg' in locals() else False,
        'referer': referer if 'referer' in locals() else False,
    }
    return render(request, 'xml_editor.html', context)


def sipp_screen(request, pid, xml):

    log_dir = settings.BASE_DIR
    delete_old_screen_logs(log_dir)

    cport = request.GET.get('cp')
    mcalls = request.GET.get('m')
    context = {
        'xml':xml,
        'pid':pid,
        'cport':cport,
        'mcalls': mcalls,
        }
    return render(request, 'sipp_screen.html', context)
    

def create_scenario_xml_view(request):
    if request.method == 'POST':
        xmlContent=request.POST.get('xml_content')
        fileName=request.POST.get('file_name')
        cleanedFilename = clean_filename(fileName)
        xml_dir = Path(settings.BASE_DIR) / 'easySIPp' / 'xml'
        with open(xml_dir / cleanedFilename, 'w', encoding='utf-8') as file:
            file.write(xmlContent)
    
    context = {
        'xml_content':xmlContent if 'xmlContent' in locals() else False,
        'xml_name':fileName if 'fileName' in locals() else False,
    }

    return render(request, 'create_scenario_xml.html', context)


def xml_mgmt_view(request):
    xml_dir = Path(settings.BASE_DIR) / 'easySIPp' / 'xml'
    xmlUploadF = xmlUploadForm()

    if request.method == 'POST' and 'submitType' in request.POST:
        submitType = request.POST.get('submitType')
        if submitType == 'upload':
            xmlUploadF = xmlUploadForm(request.POST, request.FILES)
            if xmlUploadF.is_valid():
                uploaded_file = request.FILES['file']
                cleaned_filename = clean_filename(uploaded_file.name)
                file_path = xml_dir / cleaned_filename
                
                # Validate the uploaded XML file
                # if file name already exists, do not overwrite, show error
                if file_path.exists():
                    uploadMsg = f"File '{cleaned_filename}' already exists. Rename your file and try again."
                 
                else:
                    try:
                        with open(file_path, 'wb+') as destination:
                            for chunk in uploaded_file.chunks():
                                destination.write(chunk)
                        tree = ET.parse(str(file_path))
                        uploadMsg = f"File '{cleaned_filename}' uploaded successfully."
                    
                    except ET.ParseError as e:
                        file_path.unlink(missing_ok=True)
                        uploadMsg = f"Invalid XML file '{uploaded_file.name}': {e}"

    if request.method =='GET' and 'delete' in request.GET:
        deleteXmlName=request.GET.get('delete')
        deleteXmlPath = xml_dir / deleteXmlName
        if deleteXmlPath.exists():
            deleteXmlPath.unlink()
        
    uacList, uasList = list_xml_files(str(xml_dir))
    context = {
        'uac_list':uacList, 'uas_list':uasList,
        'xml_upload_form': xmlUploadF,
        'upload_msg': uploadMsg if 'uploadMsg' in locals() else False,
        }
    
    return render(request, 'xml_management.html', context)
