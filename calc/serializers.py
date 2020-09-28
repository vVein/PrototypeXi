from rest_framework import serializers
from .models import Pipes

class PipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipes
        fields = ['pipe_id','upstream_node','downstream_node','pipe_size','pipe_length','discharge','upstream_invert',
        'downstream_invert','project_id', 'system', 'order','design_upstream_invert','design_downstream_invert',
         'design_gradient', 'upstream_structure_drop_structure']