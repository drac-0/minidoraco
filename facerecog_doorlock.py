from cvzone.HandTrackingModule import HandDetector
import cv2
import face_recognition
from time import sleep
import pyfirmata

board = pyfirmata.Arduino('COM3') 
RELAY = 9   
board.digital[RELAY].mode = 1   
pin12 = board.get_pin('d:12:o')
encoding_wajah = []
file_path = "your path blablabla"
foto = face_recognition.load_image_file(file_path)
encoding_foto = face_recognition.face_encodings(foto)[0]
encoding_wajah.append(encoding_foto)
video = cv2.VideoCapture(0)

pin2 = board.get_pin('d:2:i')
pin3 = board.get_pin('d:3:i')
pin4 = board.get_pin('d:4:i')
pin5 = board.get_pin('d:5:i')
it = pyfirmata.util.Iterator(board)
it.start()
pin2.enable_reporting()
pin3.enable_reporting()
pin4.enable_reporting()
pin5.enable_reporting()
passwordlist = [2,1,2,4,1,1,3,3,4]
checklist = []
while len(passwordlist) != len(checklist) :
    conpin2 = pin2.read()
    conpin3 = pin3.read()
    conpin4 = pin4.read()
    conpin5 = pin5.read()
    sleep(0.1)
    print(checklist) 
    if conpin2  :
        checklist.append(1)
        sleep(0.3)
        
    elif conpin3  :
        checklist.append(2)
        sleep(0.3)
        
    elif conpin4  :
        checklist.append(3)
        sleep(0.3)
        
    elif conpin5  :
        checklist.append(4)
        sleep(0.3)
        
    else :
        continue

def wajah() :
    bataswaktu = 0
    hitung = 0
    while True:
        ret, frame = video.read()
        if not ret :
            print("tidak bisa membaca frame")
            break

        lokasi_wajah = face_recognition.face_locations(frame)
        encode = face_recognition.face_encodings(frame, lokasi_wajah)

        if len(lokasi_wajah) == 0 :
            bataswaktu += 1
            print(f"bataswaktu anda {7 - bataswaktu}")
            if bataswaktu == 7 :
                video.release()
                return False

        for (top, right, bottom, left), encoding_wajah in zip(lokasi_wajah, encode) :
            matches = face_recognition.compare_faces([encoding_foto], encoding_wajah)
            if True in matches :
                cv2.rectangle(frame, (left,top), (right,bottom), (0,0,255), 2)
                cv2.putText(frame, "MENGONFIRMASI", (left - 35, top - 35), cv2.FONT_HERSHEY_COMPLEX, 0.9 , (0,0,255),2)
                cv2.putText(frame, "WAJAH", (left, top - 10), cv2.FONT_HERSHEY_COMPLEX, 0.9 , (0,0,255),2)
                hitung += 1
                print(hitung)
                if hitung == 5 :
                    video.release()
                    return True  
  
            elif True not in matches :
                cv2.rectangle(frame, (left,top), (right,bottom), (0,0,255), 2)
                cv2.putText(frame, "TIDAK", (left, top - 35), cv2.FONT_HERSHEY_COMPLEX, 0.9 , (0,0,255),2)
                cv2.putText(frame, "DIKETAHUI", (left, top - 10), cv2.FONT_HERSHEY_COMPLEX, 0.9 , (0,0,255),2)
                bataswaktu += 1
                print(f"bataswaktu anda {7 - bataswaktu}")
                if bataswaktu == 7 :
                    video.release()
                    return False

        cv2.imshow("VIDEO", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') :
            break

def tangan() :
    bataswaktu = 0
    detector=HandDetector(detectionCon=0.8,maxHands=1)
    video=cv2.VideoCapture(0)

    #[jempol,telunjuk,tengah,manis,kelingking]
    pass1 = [1,1,1,0,0]
    pass2 = [1,1,0,0,1]
    pass3 = [0,1,0,0,0]
    pass4 = [0,1,1,1,0]
    pass5 = [1,1,1,1,1]
    actualpass = [pass1, pass2, pass3, pass4, pass5]
    checkpass = []
    a = 0
    while len(actualpass) != len(checkpass) and bataswaktu != 6:
        ret, frame = video.read()
        frame = cv2.flip(frame,1)
        hands,img  = detector.findHands(frame)
        if hands:
            lmList=hands[0]
            hitung_jari=detector.fingersUp(lmList)
            print(checkpass)

            if hitung_jari == pass1 and a == 0 :
                checkpass.append(pass1)
                a += 1
                
            elif hitung_jari == pass2 and a == 1:
                checkpass.append(pass2)
                a += 1

            elif hitung_jari == pass3 and a == 2:
                checkpass.append(pass3)
                a += 1

            elif hitung_jari == pass4 and a == 3:
                checkpass.append(pass4)
                a += 1

            elif hitung_jari == pass5 and a == 4:
                checkpass.append(pass5)
                a += 1


        cv2.imshow("frame",frame)
        k=cv2.waitKey(1)

    if actualpass == checkpass :        
        video.release()
        cv2.destroyAllWindows()
        return True

    else :
        video.release()
        cv2.destroyAllWindows()
        return True


hasil = wajah() and checklist == passwordlist and tangan()
print(f"Status : {hasil}")

if hasil:
    print("Mengaktifkan relay...")
    board.digital[RELAY].write(1)  
    sleep(5)
    board.digital[RELAY].write(0)
    print("Relay dimatikan kembali.")

else:
    print("Wajah tidak dikenali, relay tetap mati.")
    pin12.write(1)
    sleep(5) 

    pin12.write(0)
