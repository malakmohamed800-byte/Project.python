from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os

def create_egypt_welcome_design():
    """
    إنشاء صورة Welcome to Egypt مع الأزرار
    بنفس تصميم المثال السابق
    """
    
    # أبعاد الصورة (بنفس أبعاد المثال)
    width, height = 1200, 700
    
    # 1. إنشاء الخلفية الأساسية
    print("🎨 جاري إنشاء الخلفية...")
    
    # إنشاء خلفية بتدرج أزرق داكن (لون النيل والسماء)
    base_color = (12, 35, 64)  # أزرق مصري داكن
    image = Image.new('RGB', (width, height), color=base_color)
    draw = ImageDraw.Draw(image)
    
    # إضافة تدرج لوني للسماء
    for y in range(height // 2):
        factor = y / (height // 2)
        r = int(12 + factor * 40)
        g = int(35 + factor * 60)
        b = int(64 + factor * 90)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 2. إضافة نجوم لامعة
    print("✨ جاري إضافة النجوم...")
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height // 3)
        size = random.uniform(0.5, 2.5)
        brightness = random.randint(180, 255)
        twinkle = random.randint(200, 255)
        draw.ellipse(
            [(x - size, y - size), (x + size, y + size)],
            fill=(brightness, brightness, twinkle)
        )
    
    # 3. إضافة شمس ذهبية
    print("☀️ جاري إضافة الشمس...")
    sun_center = (200, 150)
    sun_radius = 60
    
    # إنشاء صورة شفافة للشمس
    sun_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    sun_draw = ImageDraw.Draw(sun_layer)
    
    # طبقات الشمس (لتأثير التوهج)
    for i in range(10, 0, -1):
        radius = sun_radius + i * 5
        alpha = 30 - i * 3
        color = (255, 215, 0, alpha)  # ذهبي مع شفافية
        sun_draw.ellipse(
            [
                (sun_center[0] - radius, sun_center[1] - radius),
                (sun_center[0] + radius, sun_center[1] + radius)
            ],
            fill=color
        )
    
    # الشمس الأساسية
    sun_draw.ellipse(
        [
            (sun_center[0] - sun_radius, sun_center[1] - sun_radius),
            (sun_center[0] + sun_radius, sun_center[1] + sun_radius)
        ],
        fill=(255, 223, 0)  # ذهبي
    )
    
    # دمج الشمس مع الصورة
    image = Image.alpha_composite(image.convert('RGBA'), sun_layer).convert('RGB')
    draw = ImageDraw.Draw(image)
    
    # 4. إضافة نهر النيل
    print("🌊 جاري إضافة نهر النيل...")
    nile_color = (30, 144, 255)  # أزرق النيل
    
    # مسار متعرج للنهر
    river_width = 300
    river_start_y = height // 2 - 50
    
    points = []
    for x in range(0, width + 50, 50):
        y_offset = 50 * (x / width) * random.uniform(0.8, 1.2)
        points.append((x, river_start_y + y_offset))
    
    # رسم النهر
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        
        # الخط الرئيسي
        draw.line([(x1, y1), (x2, y2)], fill=nile_color, width=river_width)
        
        # إضافة تموجات
        for j in range(5):
            wave_y = y1 + random.randint(-5, 5)
            wave_color = (min(255, nile_color[0] + 20), 
                         min(255, nile_color[1] + 20), 
                         min(255, nile_color[2] + 20))
            draw.line([(x1, wave_y), (x2, wave_y)], fill=wave_color, width=3)
    
    # 5. إضافة الصحراء والرمال
    print("🏜️ جاري إضافة الصحراء...")
    sand_start = height // 2 + 100
    
    # تدرج لون الرمال
    sand_colors = [
        (210, 180, 140),  # رمال فاتحة
        (194, 178, 128),  # رمال متوسطة
        (139, 119, 101)   # رمال داكنة
    ]
    
    for y in range(sand_start, height):
        progress = (y - sand_start) / (height - sand_start)
        
        # اختيار اللون بناء على الارتفاع
        if progress < 0.3:
            sand_color = sand_colors[0]
        elif progress < 0.7:
            sand_color = sand_colors[1]
        else:
            sand_color = sand_colors[2]
        
        # إضافة تموجات رملية
        for x in range(0, width, 100):
            wave_height = random.randint(1, 5)
            for wy in range(wave_height):
                shade_factor = 1 - (wy * 0.1)
                shaded_color = tuple(int(c * shade_factor) for c in sand_color)
                draw.line(
                    [(x, y + wy), (x + 100, y + wy)],
                    fill=shaded_color,
                    width=1
                )
    
    # 6. إضافة الأهرامات
    print("🔺 جاري إضافة الأهرامات...")
    
    # الهرم الأكبر (خوفو)
    pyramid1_points = [
        (width - 350, sand_start + 50),  # القمة
        (width - 600, height),           # اليسار
        (width - 100, height)            # اليمين
    ]
    draw.polygon(pyramid1_points, fill='#C19A6B', outline='#8B4513', width=3)
    
    # إضافة خطوط الهرم
    for i in range(5):
        y = sand_start + 50 + i * ((height - sand_start - 50) // 5)
        x1 = width - 350 - (y - sand_start - 50) * 2.5
        x2 = width - 350 + (y - sand_start - 50) * 2.5
        draw.line([(x1, y), (x2, y)], fill='#8B4513', width=1)
    
    # الهرم الأوسط (خفرع)
    pyramid2_points = [
        (width - 550, sand_start + 80),
        (width - 750, height),
        (width - 350, height)
    ]
    draw.polygon(pyramid2_points, fill='#D2B48C', outline='#A0522D', width=3)
    
    # الهرم الصغير (منقرع)
    pyramid3_points = [
        (width - 200, sand_start + 30),
        (width - 400, height),
        (width - 0, height)
    ]
    draw.polygon(pyramid3_points, fill='#E6D3A7', outline='#8B7355', width=3)
    
    # 7. إضافة طبقة داكنة شفافة فوق الخلفية
    print("🎭 جاري إضافة الطبقة الشفافة...")
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 120))  # 47% شفافية
    image = Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(image)
    
    # 8. إضافة النص الرئيسي "WELCOME TO EGYPT"
    print("🔤 جاري إضافة النص الرئيسي...")
    
    # محاولة استخدام خطوط مختلفة
    font_paths = [
        "arialbd.ttf", "arial.ttf", "timesbd.ttf", 
        "C:\\Windows\\Fonts\\arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]
    
    title_font = None
    subtitle_font = None
    button_font = None
    
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                title_font = ImageFont.truetype(font_path, 80)
                subtitle_font = ImageFont.truetype(font_path, 28)
                button_font = ImageFont.truetype(font_path, 24)
                print(f"✓ تم تحميل الخط من: {font_path}")
                break
        except:
            continue
    
    if title_font is None:
        print("⚠️  استخدام الخط الافتراضي")
        title_font = ImageFont.load_default()
        title_font.size = 80
        subtitle_font = ImageFont.load_default()
        subtitle_font.size = 28
        button_font = ImageFont.load_default()
        button_font.size = 24
    
    # النص الرئيسي مع تأثير الظل
    title_text = "WELCOME TO EGYPT"
    
    # حساب موقع النص في المنتصف
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = (width - text_width) // 2
    text_y = height // 3 - text_height // 2
    
    # إضافة الظل (متعدد الطبقات لمزيد من الوضوح)
    shadow_colors = [
        (0, 0, 0, 100),    # ظل داكن قريب
        (0, 0, 0, 50),     # ظل متوسط
        (0, 0, 0, 20)      # ظل خفيف
    ]
    
    for i, (shadow_color) in enumerate(shadow_colors):
        offset = 2 + i * 1.5
        # إنشاء طبقة شفافة للظل
        shadow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_layer)
        shadow_draw.text(
            (text_x + offset, text_y + offset),
            title_text,
            font=title_font,
            fill=shadow_color
        )
        image = Image.alpha_composite(image.convert('RGBA'), shadow_layer)
    
    image = image.convert('RGB')
    draw = ImageDraw.Draw(image)
    
    # إضافة النص الرئيسي (الأبيض)
    draw.text(
        (text_x, text_y),
        title_text,
        font=title_font,
        fill=(255, 255, 255)  # أبيض نقي
    )
    
    # 9. إضافة النص الثانوي
    subtitle_text = "Land of Pharaohs, Pyramids & Ancient Civilization"
    bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = text_y + text_height + 30
    
    draw.text(
        (subtitle_x, subtitle_y),
        subtitle_text,
        font=subtitle_font,
        fill=(255, 215, 0)  # ذهبي
    )
    
    # 10. إضافة الأزرار
    print("🔘 جاري إضافة الأزرار...")
    
    # تعريف أبعاد وألوان الأزرار
    button_width, button_height = 220, 55
    button_y = subtitle_y + 80
    
    # زر "GET STARTED"
    get_started_x = (width // 2) - button_width - 20
    
    # إنشاء زر Get Started (برتقالي متدرج)
    # الرسم في طبقة منفصلة للتدرج
    button1_layer = Image.new('RGBA', (button_width, button_height), (0, 0, 0, 0))
    button1_draw = ImageDraw.Draw(button1_layer)
    
    # تدرج لوني للزر
    for i in range(button_height):
        factor = i / button_height
        r = int(255 - factor * 20)  # برتقالي داكن في الأسفل
        g = int(140 - factor * 40)
        b = 0
        button1_draw.line([(0, i), (button_width, i)], fill=(r, g, b))
    
    # زوايا دائرية
    button1_draw.rounded_rectangle(
        [(0, 0), (button_width, button_height)],
        radius=25,
        fill=None,
        outline=(255, 255, 255, 180),
        width=2
    )
    
    # إضافة النص على الزر
    bbox = button1_draw.textbbox((0, 0), "GET STARTED", font=button_font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x_btn = (button_width - text_w) // 2
    text_y_btn = (button_height - text_h) // 2 - 5
    
    button1_draw.text(
        (text_x_btn, text_y_btn),
        "GET STARTED",
        font=button_font,
        fill=(255, 255, 255)
    )
    
    # لصق الزر على الصورة الرئيسية
    image.paste(
        button1_layer.convert('RGB'), 
        (get_started_x, button_y), 
        button1_layer
    )
    
    # زر "ABOUT US"
    about_us_x = (width // 2) + 20
    
    # إنشاء زر About Us (شفاف بإطار)
    button2_layer = Image.new('RGBA', (button_width, button_height), (0, 0, 0, 0))
    button2_draw = ImageDraw.Draw(button2_layer)
    
    # إطار أبيض فقط
    button2_draw.rounded_rectangle(
        [(0, 0), (button_width, button_height)],
        radius=25,
        fill=None,
        outline=(255, 255, 255, 220),
        width=3
    )
    
    # إضافة النص على الزر
    bbox = button2_draw.textbbox((0, 0), "ABOUT US", font=button_font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x_btn = (button_width - text_w) // 2
    text_y_btn = (button_height - text_h) // 2 - 5
    
    button2_draw.text(
        (text_x_btn, text_y_btn),
        "ABOUT US",
        font=button_font,
        fill=(255, 255, 255)
    )
    
    # لصق الزر على الصورة الرئيسية
    image.paste(
        button2_layer.convert('RGB'), 
        (about_us_x, button_y), 
        button2_layer
    )
    
    # 11. إضافة تأثيرات نهائية
    print("🎆 جاري إضافة اللمسات النهائية...")
    
    # تأثير ضبابي خفيف جداً
    image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # زيادة التباين قليلاً
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.1)
    
    # زيادة الإشباع
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.2)
    
    # 12. حفظ الصورة
    print("💾 جاري حفظ الصورة...")
    
    # إنشاء مجلد إذا لم يكن موجوداً
    if not os.path.exists("output"):
        os.makedirs("output")
    
    output_path = "output/welcome_to_egypt_final.jpg"
    image.save(output_path, "JPEG", quality=95, optimize=True)
    
    print(f"\n✅ تم إنشاء الصورة بنجاح!")
    print(f"📁 تم حفظها في: {os.path.abspath(output_path)}")
    print(f"📏 الأبعاد: {width} × {height} بيكسل")
    print(f"🎨 نوع الملف: JPEG")
    
    # عرض الصورة (إذا كان النظام يدعم ذلك)
    try:
        image.show()
        print("👁️  تم عرض الصورة تلقائياً.")
    except:
        print("ℹ️  افتح الملف يدوياً لعرض الصورة.")
    
    return image, output_path

# تشغيل البرنامج
if __name__ == "__main__":
    print("=" * 50)
    print("       مولد صورة Welcome to Egypt       ")
    print("=" * 50)
    print("\n⚡ هذا البرنامج سينشئ لك صورة تحتوي على:")
    print("   ✓ خلفية مصرية (سماء، نيل، صحراء، أهرامات)")
    print("   ✓ نص 'WELCOME TO EGYPT' كبير في المنتصف")
    print("   ✓ زرين: GET STARTED و ABOUT US")
    print("   ✓ تأثيرات بصرية جذابة")
    print("\n" + "=" * 50)
    
    try:
        # إنشاء الصورة
        final_image, output_path = create_egypt_welcome_design()
        
        print("\n" + "=" * 50)
        print("🎉 تم الانتهاء من إنشاء الصورة!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ حدث خطأ: {e}")
        print("يرجى التأكد من تثبيت المكتبات المطلوبة:")
        print("pip install pillow")
