/* ภาพจำลอง UI เวกเตอร์ (ใช้แทนภาพหน้าจอในหน้าขั้นตอน) — .hot = จุดที่ต้องกด */
P.plus='<path d="M12 5v14M5 12h14"/>';
P.check='<path d="M20 6 9 17l-5-5"/>';
P.pdf='<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/>';
P.shutter='<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/>';
const hot=(h,on)=>on?`<span class="hot">${h}</span>`:h;
const win=(url,body)=>`<div class="mk-win"><div class="mk-bar"><i></i><i></i><i></i><span>${url}</span></div><div class="mk-body">${body}</div></div>`;
const drive=({crumb,rows=[],menu=null,newHot=false})=>win('drive.google.com',
 `<div class="mk-drive"><div class="mk-side">${hot(`<div class="mk-new">${I('plus')}ใหม่</div>`,newHot)}<div class="mk-nav">ไดรฟ์ของฉัน</div><div class="mk-nav o">แชร์กับฉัน</div><div class="mk-nav o">ล่าสุด</div></div>
 <div class="mk-main"><div class="mk-crumb">${crumb}</div>`+rows.map(([ic,t,h])=>`<div class="mk-row">${hot(`<span class="mk-rc">${I(ic)}${t}</span>`,h)}</div>`).join('')+`</div>`+
 (menu?`<div class="mk-menu">`+menu.map(([ic,t,h])=>`<div class="mk-mi">${hot(`<span class="mk-rc">${I(ic)}${t}</span>`,h)}</div>`).join('')+`</div>`:'')+`</div>`);
const phone=(title,body)=>`<div class="mk-phone"><div class="mk-notch"></div><div class="mk-ptitle">${title}</div><div class="mk-pbody">${body}</div></div>`;
const gn=body=>win('notebook.google',`<div class="mk-gn">${body}</div>`);

const MK={
 'drive-folder':drive({crumb:'ไดรฟ์ของฉัน › <b>งานวิจัย พุทธจิตวิทยา</b>',rows:[['folder','01 เปเปอร์ ThaiJO',1],['folder','02 สแกนหนังสือ']]}),
 'drive-menu':drive({crumb:'… › <b>01 เปเปอร์ ThaiJO</b>',newHot:1,menu:[['folder','โฟลเดอร์ใหม่'],['upload','อัปโหลดไฟล์',1],['folder','อัปโหลดโฟลเดอร์']]}),
 'drive-files':drive({crumb:'… › <b>01 เปเปอร์ ThaiJO</b>',rows:[['pdf','2564 สมเจตน์ พุทธจิตวิทยา.pdf',1],['pdf','2565 พระมหา… สติ.pdf'],['pdf','2566 กิตติ… สมาธิ.pdf']]}),
 'phone-scan':phone('Google ไดรฟ์',`<div class="mk-pl">ไฟล์ล่าสุด</div><div class="mk-pline"></div><div class="mk-pline s"></div><div class="mk-sheet"><div class="mk-si">${I('upload')}อัปโหลด</div><div class="mk-si">${hot(`<span class="mk-rc">${I('camera')}สแกน</span>`,1)}</div><div class="mk-si">${I('folder')}โฟลเดอร์</div></div>`),
 'phone-shoot':phone('สแกน',`<div class="mk-page"><div class="mk-pline"></div><div class="mk-pline"></div><div class="mk-pline s"></div><div class="mk-pline"></div></div><div class="mk-shoot">${hot(`<span class="mk-shut">${I('shutter')}</span>`,1)}<span class="mk-add">${I('plus')}เพิ่มหน้า</span></div>`),
 'phone-save':phone('บันทึกลงในไดรฟ์',`<div class="mk-field"><small>ชื่อไฟล์</small>หนังสือ พุทธจิตวิทยา บทที่ 2</div><div class="mk-field">${hot(`<span class="mk-rc">${I('folder')}02 สแกนหนังสือ</span>`,1)}<small>โฟลเดอร์</small></div><div class="mk-btn">บันทึก</div>`),
 'gn-new':gn(`<div class="mk-gnh">โน้ตบุ๊กของฉัน</div><div class="mk-cards">${hot(`<div class="mk-card n">${I('plus')}สร้างใหม่</div>`,1)}<div class="mk-card"></div><div class="mk-card"></div></div>`),
 'gn-add':gn(`<div class="mk-gnh">เพิ่มแหล่งข้อมูล</div><div class="mk-opts"><div class="mk-opt">${I('upload')}อัปโหลดไฟล์</div>${hot(`<div class="mk-opt">${I('folder')}Google ไดรฟ์</div>`,1)}<div class="mk-opt">${I('link')}เว็บไซต์</div><div class="mk-opt">${I('copy')}ข้อความที่คัดลอก</div></div>`),
 'gn-pick':gn(`<div class="mk-gnh">งานวิจัย พุทธจิตวิทยา</div>`+[['01 เปเปอร์ ThaiJO · 3 ไฟล์'],['02 สแกนหนังสือ · 1 ไฟล์']].map(([t])=>`<div class="mk-row"><span class="mk-rc"><span class="mk-cb">${I('check')}</span>${I('folder')}${t}</span></div>`).join('')+`<div class="mk-btn r">${hot('เลือก',1)}</div>`),
 'gn-sources':gn(`<div class="mk-gnh">แหล่งข้อมูล · 4</div>`+['2564 สมเจตน์ พุทธจิตวิทยา','2565 พระมหา… สติ','2566 กิตติ… สมาธิ','หนังสือ พุทธจิตวิทยา บทที่ 2'].map(t=>`<div class="mk-row"><span class="mk-rc"><span class="mk-cb">${I('check')}</span>${I('pdf')}${t}</span></div>`).join('')),
 'gn-answer':gn(`<div class="mk-q">ทำตารางเปรียบเทียบ ผู้แต่ง ปี วิธีวิจัย</div><div class="mk-a"><p>งานทั้ง 3 เรื่องใช้การวิจัยเชิงคุณภาพ ${hot('<span class="mk-cite">1</span>',1)} ต่างจากบทที่ 2 ของหนังสือที่เน้นหลักธรรม ${hot('<span class="mk-cite">4</span>',1)}</p><div class="mk-pline"></div><div class="mk-pline s"></div></div>`)
};
