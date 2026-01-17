# app_customers/forms.py

from django import forms

class CustomerOrderForm(forms.Form):
    """Formulario para capturar datos del cliente en el checkout"""
    
    customer_name = forms.CharField(
        max_length=255,
        required=True,
        label='Nombre Completo'
    )
    
    customer_phone = forms.CharField(
        max_length=20,
        required=True,
        label='Teléfono / WhatsApp'
    )
    
    customer_email = forms.EmailField(
        required=False,
        label='Email'
    )
    
    department = forms.CharField(
        max_length=100,
        required=True,
        label='Departamento'
    )
    
    city = forms.CharField(
        max_length=100,
        required=True,
        label='Ciudad'
    )
    
    neighborhood = forms.CharField(
        max_length=100,
        required=False,
        label='Barrio'
    )
    
    address = forms.CharField(
        max_length=255,
        required=True,
        label='Dirección Completa'
    )
    
    note = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label='Observaciones'
    )
    
    def clean_customer_phone(self):
        """Validar formato de teléfono colombiano"""
        phone = self.cleaned_data.get('customer_phone')
        phone = ''.join(filter(str.isdigit, phone))
        
        if len(phone) != 10:
            raise forms.ValidationError('El teléfono debe tener 10 dígitos')
        
        if not phone.startswith('3'):
            raise forms.ValidationError('Debe ser un celular colombiano (empezar con 3)')
        
        return phone
    
    def clean_customer_name(self):
        """Validar nombre"""
        name = self.cleaned_data.get('customer_name')
        
        if len(name.strip()) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres')
        
        return name.strip()