from rest_framework import serializers
from .models import Cliente, Barbero, Servicio


class ClienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'apellido', 'nombre_completo']
    
    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}".strip()


class ClienteRegistroSerializer(serializers.ModelSerializer):
    contraseña = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'celular', 'correo', 'contraseña']
    
    def create(self, validated_data):
        cliente = Cliente(**validated_data)
        cliente.set_password(validated_data['contraseña'])
        cliente.save()
        return cliente


class BarberoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbero
        fields = ['id', 'nombre']


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'precio']


class CitaCreateSerializer(serializers.Serializer):
    cliente_id = serializers.IntegerField(min_value=1)
    barbero_id = serializers.IntegerField(min_value=1)
    servicio_id = serializers.IntegerField(min_value=1)
    fecha = serializers.DateTimeField()
    tipo = serializers.ChoiceField(choices=["normal", "premium"], required=False, default="normal")


class CitaResponseSerializer(serializers.Serializer):
    msg = serializers.CharField()
    cita_id = serializers.IntegerField(min_value=1)

class ClienteLoginSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    contraseña = serializers.CharField(write_only=True)


class ClienteLoginResponseSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'apellido', 'nombre_completo', 'correo', 'celular']
    
    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}".strip()


class ClienteRegistroResponseSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'apellido', 'nombre_completo', 'correo', 'celular']
    
    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}".strip()
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['msg'] = "Cliente registrado exitosamente"
        return data