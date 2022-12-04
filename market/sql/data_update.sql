update timetable
set status = 'busy'
where id_d = '$doctor_id'
      and date_zap = '$date_zap'
      and time_zap = '$time_zap';