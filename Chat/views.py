from django.shortcuts import render , redirect , HttpResponse
from .models import Room
# Create your views here.

def chat_rooms(request):
    rooms = Room.objects.all()  # ดึงใช้เพื่อดึงรายการห้องแชททั้งหมดจากโมเดล Room
    return render(request, 'chat_rooms.html', {'rooms': rooms}) #ส่งผลลัพธ์ของห้องแชททั้งหมดไปยังเทมเพลต

def chat_room(request, room_name): #ฟังก์ชันนี้ใช้เพื่อให้ผู้ใช้เข้าร่วมห้องแชทตามชื่อห้อง
    return render(request, 'Chatpage.html', {
        'room_name': room_name #ส่งค่าชื่อห้อง (room_name) ไปยังเทมเพลต Chatpage.html
    }) 

def create_room(request):
    if request.method == 'POST': #ตรวจสอบว่าผู้ใช้กำลังส่งแบบฟอร์มผ่าน HTTP POST
        room_name = request.POST.get('room_name') # ดึงค่าชื่อห้องที่ผู้ใช้ป้อนเข้ามาในแบบฟอร์ม
        if Room.objects.filter(name=room_name).exists(): # ตรวจสอบในฐานข้อมูลว่ามีห้องชื่อนี้อยู่แล้วหรือไม่
            return HttpResponse('Room already exists!')
        room = Room.objects.create(name=room_name)  #สร้างห้องใหม่ในฐานข้อมูลด้วยชื่อห้อง
        return redirect('chat_rooms', room_name=room.name) #หลังจากสร้างห้องแล้ว จะทำการเปลี่ยนเส้นทางไปยังหน้า chat_rooms
    return render(request, 'create_room.html')