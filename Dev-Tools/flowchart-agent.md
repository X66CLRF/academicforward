flowchart TD
    %% กำหนดสไตล์กล่อง: ขาวดำ, เส้นหนา, ฟอนต์ TH Sarabun New ขนาด 18px
    classDef boxStyle fill:#ffffff,stroke:#000000,stroke-width:2px,font-family:'TH Sarabun New',font-size:18px;

    %% รายการกล่องข้อความขั้นตอนการทำงาน
    A([เริ่มต้น]):::boxStyle
    B[/รับคำสั่ง/คำถามจากผู้ใช้ User Request/]:::boxStyle
    C[Agent กลางวิเคราะห์โจทย์และเจตนา Intent Classification]:::boxStyle
    D[วางแผนการทำงานและเลือกเครื่องมือหรือ Agent ที่เหมาะสม Task Planning]:::boxStyle
    
    %% ขั้นตอนการตัดสินใจและการลูปทำงาน
    E{จำเป็นต้องใช้<br>เครื่องมือภายนอกไหม?}:::boxStyle
    F[ส่งงานให้ Agent เฉพาะทาง / ดึงข้อมูลจาก Tools หรือ API]:::boxStyle
    G[รับข้อมูลกลับมาตรวจสอบความถูกต้องและรวบรวมผลลัพธ์]:::boxStyle
    H[ประมวลผลและเรียบเรียงคำตอบฉบับสมบูรณ์]:::boxStyle
    I[/ส่งคำตอบกลับไปให้ผู้ใช้ User Response/]:::boxStyle
    Z([สิ้นสุด]):::boxStyle

    %% การเชื่อมต่อเส้น
    A --> B
    B --> C
    C --> D
    D --> E
    
    %% เงื่อนไขเงื่อนไข Yes / No
    E -- ใช่ --> F
    F --> G
    G --> D %% วนกลับไปคิดต่อว่าต้องทำอะไรเพิ่มไหม (ReAct Pattern)
    
    E -- ไม่ --> H
    H --> I
    I --> Z

    %% กำหนดสไตล์เส้นลูกศรทั้งหมดให้เป็นสีดำและหนา
    linkStyle default stroke:#000000,stroke-width:2px;