from django.db import models
from django.forms import ModelForm

# Create your models here.

class Project (models.Model):
    project_id = models.CharField(max_length = 12)

    def __str__(self):
        return self.project_id

class Structures (models.Model):

    structure_id = models.CharField(max_length = 20)
    type_and_size = models.CharField(max_length = 20)
    surface_elevation = models.DecimalField(max_digits=19, decimal_places=2)
    project_id = models.CharField(max_length = 20, default = "0000")

    def __str__(self):
        return self.structure_id

class Pipes (models.Model):

    pipe_id = models.CharField(max_length = 20)
    upstream_node = models.CharField(max_length = 20)
    downstream_node = models.CharField(max_length = 20)
    pipe_size = models.CharField(max_length = 30)
    pipe_length = models.DecimalField(max_digits=15, decimal_places=3)
    discharge = models.DecimalField(max_digits=15, decimal_places=3)
    upstream_invert = models.DecimalField(max_digits=15, decimal_places=3)
    downstream_invert = models.DecimalField(max_digits=15, decimal_places=3)
    project_id = models.CharField(max_length = 20, default = "0000")
    system = models.IntegerField(default = "0")
    order = models.IntegerField(default = "0")
    design_upstream_invert = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    design_downstream_invert = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    design_gradient = models.DecimalField(max_digits=10, decimal_places=3, default = 0.01)

    def __str__(self):
        return self.pipe_id

#pipe_range = ['18','24','30','36','42','48','54','60','72','78']

class Generic_Structures (models.Model):

    structure_type = models.CharField(max_length = 20)
    drop_across_bottom = models.DecimalField(max_digits=19, decimal_places=2)
    maximum_depth = models.DecimalField(max_digits=19, decimal_places=2)
    minimum_depth_18_inch = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    minimum_depth_24_inch = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    minimum_depth_30_inch = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    minimum_depth_36_inch = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    minimum_depth_42_inch = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    minimum_depth_48_inch = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    minimum_depth_54_inch = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    minimum_depth_60_inch = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    minimum_depth_72_inch = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    minimum_depth_78_inch = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
#    pass

#for pipe_size_data in pipe_range:
#    field_name = '{}_inch_minimum_depth'.format(pipe_size_data)
#    Generic_Structures.add_to_class(field_name, models.DecimalField(max_digits=15, decimal_places=2, null = True, default = 'Nan'))

    def __str__(self):
        return self.structure_type