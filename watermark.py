
from moviepy.editor import *
import moviepy.editor as mpy


video1 = mpy.VideoFileClip("video.mp4")  # Путь к файлу
video1_re = video1.resize(width=720)

# logo = (ImageClip("smile.jpeg", transparent=True)  # Ваш логотип
#         .set_duration(video1.duration)  # Устанавливаем длительность показа логотипа равную длительности всего видео
#         .resize(height=100)  # Изменяем размер картинки если нужно
#         # .margin(left=10, bottom=2, opacity=0.45)  # Необязательно: Небольшая рамка с прозрачностью
#         .set_pos(("center", "center")))  # Позиция картинки: слева по центру. Если нужно справа внизу, пишем right, bottom


# final = CompositeVideoClip([video1, logo])  # Собираем все в кучу
# final.write_videofile("video_done.mp4", audio=True)  # Записываем в финальный файл

# print(TextClip.list('font'))

txt = mpy.TextClip(f'Text in\nvideo!', font='Courier',
                   fontsize=100, color='white', bg_color='gray35', transparent=True)
txt = txt.set_position(('center', 0.6), relative=True)
txt = txt.set_start((0, 2))
txt = txt.set_duration(6)
txt = txt.crossfadein(0.5)
txt = txt.crossfadeout(0.5)

final_clip = mpy.CompositeVideoClip([video1_re, txt])


final_clip.write_videofile("video_text_done.mp4", audio=True)  # Записываем в финальный файл