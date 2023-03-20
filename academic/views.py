from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from . import models, serializers, permissions


class JurusanViewSet(ModelViewSet):
    queryset = models.Jurusan.objects.all()
    serializer_class = serializers.JurusanSerializer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [permissions.IsUptTIK()]


class SemesterViewSet(ModelViewSet):
    queryset = models.Semester.objects.all()
    serializer_class = serializers.SemesterSerializer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [permissions.IsUptTIK()]


class ProgramPendidikanViewSet(ModelViewSet):
    queryset = models.ProgramPendidikan.objects.all()
    serializer_class = serializers.ProgramPendidikanSerializer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [permissions.IsUptTIK()]


class GedungKuliahViewSet(ModelViewSet):
    queryset = models.GedungKuliah.objects.all()
    serializer_class = serializers.GedungKuliahSerializer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [permissions.IsUptTIK()]
    

class PemberitahuanViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'post', 'delete']
    queryset = models.Pemberitahuan.objects\
        .prefetch_related('filter_prodi__prodi', 'filter_jurusan__jurusan')\
        .all()
    
    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return serializers.SimplePemberitahuanSerializer
        return serializers.PemberitahuanSerializer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [permissions.IsUptTIkOrIsStaffProdi()]
    

class ProgramStudiViewSet(ModelViewSet):
    queryset = models.ProgramStudi.objects.select_related('jurusan', 'program_pendidikan').all()
    lookup_field = 'kode'
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return serializers.CreateUpdateProgramStudiSerializer
        return serializers.ProgramStudiSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'PUT':
            return [permissions.IsUptTIkOrIsStaffProdi()]
        return [permissions.IsUptTIK()]


class StaffProdiViewSet(ModelViewSet):
    queryset = models.StaffProdi.objects.select_related('prodi', 'user').all()
    lookup_field = 'no_induk'
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return serializers.CreateUpdateStaffProdiSerializer
        return serializers.StaffProdiSerializer
    
    def get_permissions(self):
        if self.action == 'retrieve' or self.request.method == 'PUT':
            return [permissions.IsUptTIkOrIsStaffProdi()]
        return [permissions.IsUptTIK()]
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateUpdateStaffProdiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff_prodi = serializer.save()
        serializer = serializers.StaffProdiSerializer(staff_prodi)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class DosenViewSet(ModelViewSet):
    queryset = models.Dosen.objects.select_related('prodi').all()
    lookup_field = 'nip'
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return serializers.CreateUpdateDosenSerializer
        return serializers.DosenSerializer

    def get_permissions(self):
        return [IsAuthenticated()] if self.request.method == 'GET' else [permissions.IsStaffProdi()]
    

class KelasViewSet(ModelViewSet):
    queryset = models.Kelas.objects\
        .select_related('prodi__jurusan', 'prodi__program_pendidikan', 'semester')\
        .all()
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return serializers.CreateUpdateKelasSerializer
        return serializers.KelasSerializer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [permissions.IsStaffProdi()]
    

class MahasiswaViewSet(ModelViewSet):
    queryset = models.Mahasiswa.objects\
        .select_related('pembimbing_akademik', 'kelas', 'kelas__prodi', 'kelas__prodi__jurusan', 'kelas__semester', 'user')\
        .all()
    lookup_field = 'nim'

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        mahasiswa, is_created = models.Mahasiswa.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = serializers.MahasiswaSerializer(mahasiswa)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = serializers.CreateUpdateMahasiswaSerializer(mahasiswa, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
                
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return serializers.CreateUpdateMahasiswaSerializer
        return serializers.MahasiswaSerializer
    
    def get_permissions(self):
        if self.action == 'me':
            return [permissions.IsMahasiswa()]
        return [permissions.IsStaffProdi()]
    

class RuanganViewSet(ModelViewSet):
    queryset = models.Ruangan.objects\
        .prefetch_related('jadwalmakul_set', 'jadwalmakul_set__dosen', 'jadwalmakul_set__mata_kuliah',
                          'jadwalmakul_set__jadwal')\
        .all()
    serializer_class = serializers.RuanganSerializer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [permissions.IsUptTIK()]
    

class AduanRuanganViewSet(ModelViewSet):
    def get_queryset(self):
        return models.AduanRuangan.objects.filter(ruangan_id=self.kwargs['ruangan_pk'])
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateAduanRuanganSerializer
        elif self.request.method == 'PUT':
            return serializers.UpdateAduanRuanganSerializer
        return serializers.AduanRuanganSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['ruangan_id'] = self.kwargs['ruangan_pk']
        return context
    
    def get_permissions(self):
        if self.request.method in ['GET', 'DELETE']:
            return [permissions.IsUptTIKOrIsMahasiswa()]
        elif self.request.method == 'PUT':
            return [permissions.IsUptTIK()]
        return [permissions.IsMahasiswa()]
    

class PemberitahuanProdiViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return serializers.CreatePemberitahuanProdiSerializer
        return serializers.PemberitahuanProdiSerializer

    def get_queryset(self):
        return models.PemberitahuanProdi.objects\
            .select_related('prodi')\
            .filter(pemberitahuan_id=self.kwargs['pemberitahuan_pk'])
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['pemberitahuan_id'] = self.kwargs['pemberitahuan_pk']
        return context
    
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [permissions.IsUptTIkOrIsStaffProdi()]
        return [permissions.IsUptTIK()]
    

class PemberitahuanJurusanViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [permissions.IsUptTIK]

    def get_queryset(self):
        return models.PemberitahuanJurusan.objects\
            .select_related('jurusan')\
            .filter(
                pemberitahuan_id=self.kwargs['pemberitahuan_pk']
            )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreatePemberitahuanJurusanSerializer
        return serializers.PemberitahuanJurusanSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['pemberitahuan_id'] = self.kwargs['pemberitahuan_pk']
        return context


class KaryaIlmiahViewSet(ModelViewSet):
    queryset = models.KaryaIlmiah.objects\
        .select_related('prodi', 'prodi__jurusan', 'prodi__program_pendidikan', 'mahasiswa', 'mahasiswa__user')\
        .all()
    serializer_class = serializers.KaryaIlmiahSerializer
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return serializers.CreateUpdateKaryaIlmiahSerializer
        return serializers.KaryaIlmiahSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'DELETE':
            return [permissions.IsStaffProdi()]
        return [permissions.IsStaffProdiOrIsMahasiswa()]
    

class JadwalViewSet(ModelViewSet):
    def get_queryset(self):
        queryset = models.Jadwal.objects\
        .select_related('kelas__prodi')\
        .prefetch_related('makul_list__dosen', 'makul_list__ruangan', 
                          'makul_list__mata_kuliah', 'makul_list__ruangan__gedung')
        kelas_id = self.request.GET.get('kelas_id', None)
        
        return queryset.filter(kelas_id=kelas_id) if kelas_id else queryset.all()
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return serializers.CreateUpdateJadwalSerializer
        return serializers.JadwalSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsStaffProdiOrIsMahasiswa()]
        return [permissions.IsStaffProdi()]
    

class MataKuliahViewSet(ModelViewSet):
    queryset = models.MataKuliah.objects.all()
    serializer_class = serializers.MataKuliahSerializer
    lookup_field = 'kode'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsStaffProdiOrIsMahasiswa()]
        return [permissions.IsStaffProdi()]


class JadwalMakulViewSet(ModelViewSet):
    queryset = models.JadwalMakul.objects\
        .select_related('dosen', 'mata_kuliah', 'ruangan__gedung')\
        .all()
    serializer_class = serializers.JadwalMakulSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['jadwal_id'] = self.kwargs['jadwal_pk']
        return context

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsStaffProdiOrIsMahasiswa()]
        return [permissions.IsStaffProdi()]
    

class KHSViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = models.KHS.objects\
        .select_related('mahasiswa__user')\
        .prefetch_related('nilai_list__mata_kuliah')\
        .all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateKHSSerializer
        return serializers.KHSSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsStaffProdiOrIsMahasiswa()]
        return [permissions.IsStaffProdi()]
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateKHSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        khs = serializer.save()
        serializer = serializers.KHSSerializer(khs)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class NilaiKHSViewSet(ModelViewSet):
    def get_queryset(self):
        return models.NilaiKHS.objects.select_related('mata_kuliah').filter(khs_id=self.kwargs['khs_pk'])
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return serializers.CreateUpdateNilaiKHSSerializer
        return serializers.NilaiKHSSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateUpdateNilaiKHSSerializer(
            data=request.data, 
            context={'khs_id': kwargs['khs_pk']}
        )
        return self.perform_save(serializer, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        serializer = serializers.CreateUpdateNilaiKHSSerializer(
            self.get_object(),
            data=request.data,
            context={'khs_id': kwargs['khs_pk']}
        )
        return self.perform_save(serializer, status=status.HTTP_200_OK)
    
    def perform_save(self, serializer, **kwargs):
        serializer.is_valid(raise_exception=True)
        try:
            nilai_khs = serializer.save()
            serializer = serializers.NilaiKHSSerializer(nilai_khs)
            return Response(serializer.data, status=kwargs['status'])
        except IntegrityError:
            return Response(
                {'mata_kuliah': ['This "mata_kuliah" is already exist in the current "khs"']}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsStaffProdiOrIsMahasiswa()]
        return [permissions.IsStaffProdi()]
    
