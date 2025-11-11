# # formatura/autocomplete.py
# from dal import autocomplete
# from django.contrib.auth.models import User
# from expedient.models import Departamento

# class ResponsavelAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         qs = User.objects.all()
#         if self.q:
#             qs = qs.filter(first_name__icontains=self.q) | qs.filter(last_name__icontains=self.q)
#         return qs

# class DepartamentoAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         qs = Departamento.objects.all()
#         if self.q:
#             qs = qs.filter(nome__icontains=self.q)
#         return qs
