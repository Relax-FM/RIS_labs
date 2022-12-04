select patient.FIO_patient as FIO_patient, patient.birthday AS birthday, doctor.FIO_doctor AS FIO_doctor
from patient, doctor
where patient.id_p = '$id_p' and doctor.id_d = '$id_d'