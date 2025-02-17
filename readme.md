<h1> Labeling for BeachGabageDetectionDataset</h1>
<h2> Install Python > 3.8.10 + </h2>
<h3> Source List </h3>
<ul>
  <li>ImageLabeling.py ใช้สำหรับทำLabeling (annotation) แบบFormat_GAnno -> Label_name x,y,w,h</li>
  <li>Convert2Yolo.py ใช้สำหรับแปลงแบบFormat_GAnno เป็น YoloV3-V5</li>
  <li>ImageCropper4Classification.py ใช้สำหรับ Crop ภาพจาก Format_GAnno แยกเป็น Folder เพื่อทำ ImageClassification </li>
</ul>
<h3> ไฟล์ต้องแปลงเป็น jpg jpeg png bmp เท่านั้น </h3>
<h1> [[[ ห้ามไฟล์ชื่อเหมือนกันซ้ำกัน แม้นามสกุลไฟล์ต่างกัน เช่น aaa.jpg กับ aaa.jpeg โปรแกรมจะทำงานผิดพลาด ]]]</h1>
<h2> การใช้งาน ImageLabeling</h2>
============= How to use =============")
<ul>
<li>Drag Mouse to crop image</li>
<li>Enter/Spacebar to save cropped box</li>
<li>Del to remove all cropped boxes in the image</li>
<li>w or / to select label</li>
<li>Esc to cancel (a) cropped box</li>
<li>←/↑ or a goto previous image</li>
<li>→/↓ or d goto next image</li>
<li>q Exit program</li>
</ul>