import threading
import winsound
import sounddevice 
import cv2
import imutils

#seting kamera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) #0 jika punya satu kamera

#mengukur frame kamera yang akan diambil
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500) #menangkap frame awal
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY) #ubah warna ke grayscale
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0) #smooth gambar

#seting alarm parameter
alarm = False #kondisi default alarm
alarm_mode = False #menunjukan deteksi alarm  
alarm_counter = 0 #menghitung jumlah frame saat deteksi gerakan

#setting outputan alarm
def beep_alarm():
    global alarm
    for _ in range(5): #loop alarm sebanyak 5x
        if not alarm_mode:
            break
        print("ALARM")
        winsound.Beep(2500, 200) #frekuensi suara saat alarm bunyi
    alarm = False


while True:

    _, frame = cap.read()
    frame = imutils.resize(frame, width=500) #Menangkap frame dari kamera dan menyesuaikannya ukuran

    #jika alarm mode aktif 
    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #konversi frame jadi grayscale
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0) #lakukan gaussian blur

        difference = cv2.absdiff(frame_bw, start_frame) #menghitung  perbedaan antara dua frame frame_bw untuk citra grayscale yang sudah diberi efek blur
        #menentukan batasan pada sudut citra menghasilkan citra treshold 
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        #mengambil start frame dari frame citra grayscale
        start_frame = frame_bw

        if threshold.sum() > 300: #jika jumlah nilai sum melebihi 300 maka terjadi atau ada gerakan
            alarm_counter += 1 #alarm akan berbunyi dan terrus bertambah 1
        else:
            if alarm_counter > 0: #jika sudah tidak ada gerakan
                alarm_counter -= 1 #alarm akan mati secara bertahap


        #jika deteksi gerakan aktif maka yang ditampilkan adalah citra hasil treshold
        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)
    

    if alarm_counter > 20: #Jika hitungan alarm (alarm_counter) lebih dari 20, ini menunjukkan bahwa gerakan telah terdeteksi 
        if not alarm:
            threading.Thread(target=beep_alarm).start()
    
    #triger alarm
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break


cap.release()
cv2.destroyAllWindows()