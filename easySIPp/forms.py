from django import forms
from django.conf import settings
import xml.etree.ElementTree as ET
import os
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import UacAppConfig, UasAppConfig

import logging
logger = logging.getLogger(__name__)

class UACForm(forms.ModelForm):
    # UAC Config Fields
    uac_key = forms.ChoiceField(
        label='Select Config',
        choices=[],  #this is set in __init__
        required=True
    )
    uac_config_name = forms.CharField(
        label='Config Name',
        required=True,
        max_length=28
    )
    uac_remote = forms.GenericIPAddressField(label='UAC Remote Address', protocol='IPv4')
    uac_remote_port = forms.IntegerField(label='UAC Remote Port', min_value=1024, max_value=65535, initial=5060)
    uac_local_addr = forms.GenericIPAddressField(label='Local Address', protocol='IPv4')
    src_port_uac = forms.IntegerField(label='UAC Src Port', min_value=1024, max_value=65535, initial=5060)
    protocol_uac = forms.ChoiceField(label='UAC Protocol', choices=[('u1', 'UDP'), ('tn', 'TCP')])

    # UAC XML Selection
    select_uac = forms.ChoiceField(label='Select UAC XML Scenario')

    # SIPp Options
    called_party_number = forms.CharField(
        label='Dialed Number',
        max_length=18,
        required=False,
        validators=[RegexValidator(r'^[a-zA-Z0-9]+$', 'Only alphanumeric characters are allowed.')]
    )
    calling_party_number = forms.CharField(
        label='Calling Party Number',
        max_length=18,
        required=False,
        validators=[RegexValidator(r'^[a-zA-Z0-9]+$', 'Only alphanumeric characters are allowed.')]
    )
    total_no_of_calls = forms.IntegerField(
        label='No. of calls to send',
        min_value=1,
        max_value=28000,
        required=True,
        initial=1
    )
    cps = forms.IntegerField(
        label='Calls Per Second',
        min_value=1,
        max_value=200,
        required=True,
        initial=1
    )
    stun_server = forms.GenericIPAddressField(
        label='STUN Server',
        protocol='IPv4',
        required=False,
        initial=''
    )

    class Meta:
        model = UacAppConfig
        fields = [
            # 'uac_key', #manually defined field
            'uac_config_name',
            'uac_remote', 'uac_remote_port',
            'uac_local_addr', 'src_port_uac', 'protocol_uac',
            'select_uac',
            'called_party_number', 'calling_party_number',
            'total_no_of_calls', 'cps', 'stun_server',
        ]

    xmlPath = str(settings.BASE_DIR / 'easySIPp' / 'xml')

    def __init__(self, *args, uac_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['select_uac'].choices = self._get_xml_file_choices('uac')
        if uac_choices:
            self.fields['uac_key'].choices = uac_choices
            self.fields['uac_key'].initial = self.instance.uac_key


    def _get_xml_file_choices(self, prefix):
        try:
            return sorted([
                (f, f) for f in os.listdir(self.xmlPath)
                if f.endswith('.xml') and f.startswith(prefix)
            ])
        except FileNotFoundError:
            return []




class UASForm(forms.ModelForm):
    # UAS Config Fields
    uas_key = forms.ChoiceField(
        label='Select Config',
        choices=[],  #this is set in __init__
        required=True
    )
    uas_config_name = forms.CharField(
        label='Config Name',
        required=True,
        max_length=28
    )
    uas_remote = forms.GenericIPAddressField(label='UAS Remote Address', protocol='IPv4')
    uas_remote_port = forms.IntegerField(label='UAS Remote Port', min_value=1024, max_value=65535, initial=5060)
    uas_local_addr = forms.GenericIPAddressField(label='Local Address', protocol='IPv4')  # Optional if shared
    src_port_uas = forms.IntegerField(label='UAS Src Port', min_value=1024, max_value=65535, initial=5060)
    protocol_uas = forms.ChoiceField(label='UAS Protocol', choices=[('u1', 'UDP'), ('tn', 'TCP')])

    # UAS XML Selection
    select_uas = forms.ChoiceField(label='Select UAS XML Scenario')

    class Meta:
        model = UasAppConfig
        fields = [
            # 'uas_key',
            'uas_config_name',
            'uas_remote', 'uas_remote_port',
            'uas_local_addr', 'src_port_uas',
            'protocol_uas', 'select_uas',
        ]

    xmlPath = str(settings.BASE_DIR / 'easySIPp' / 'xml')

    def __init__(self, *args, uas_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['select_uas'].choices = self._get_xml_file_choices('uas')
        if uas_choices:
            self.fields['uas_key'].choices = uas_choices
            self.fields['uas_key'].initial = self.instance.uas_key



    def _get_xml_file_choices(self, prefix):
        try:
            return sorted([
                (f, f) for f in os.listdir(self.xmlPath)
                if f.endswith('.xml') and f.startswith(prefix)
            ])
        except FileNotFoundError:
            return []


class xmlUploadForm(forms.Form):
    file = forms.FileField(label='Select an XML file', help_text='File name should start with "uac" or "uas".',
                           widget=forms.ClearableFileInput(attrs={'accept': '.xml', 'max_upload_size': 102400}))

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if not uploaded_file.name.lower().startswith(('uac', 'uas')) or not uploaded_file.name.lower().endswith('.xml'):
            raise ValidationError('File name should start with "uac" or "uas" and have .xml extension.')
        max_upload_size = 102400  # 100 KB in bytes
        if uploaded_file.size > max_upload_size:
            raise ValidationError('File size exceeds the maximum allowed limit (250 KB).')
        return uploaded_file
