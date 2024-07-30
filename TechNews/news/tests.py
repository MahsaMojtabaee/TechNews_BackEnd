import logging
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import News, Tag
from .serializers import NewsSerializer


logger = logging.getLogger(__name__)

class TagTests(TestCase):
    def setUp(self):
        # Create tags for tests
        self.tag1 = Tag.objects.get_or_create(name='علمی')
        self.tag2 = Tag.objects.get_or_create(name='فناوری')
        self.tag3 = Tag.objects.get_or_create(name='علوم پایه و مهندسی')
        self.tag4 = Tag.objects.get_or_create(name='مطالب موبایل')
        self.tag5 = Tag.objects.get_or_create(name='خودرو')

    def test_tag_creation(self):
        self.assertEqual(Tag.objects.count(), 5)
        self.assertEqual(Tag.objects.get(name='علمی'), self.tag1)
        self.assertEqual(Tag.objects.get(name='فناوری'), self.tag2)
        self.assertEqual(Tag.objects.get(name='علوم پایه و مهندسی'), self.tag3)
        self.assertEqual(Tag.objects.get(name='مطالب موبایل'), self.tag4)
        self.assertEqual(Tag.objects.get(name='خودرو'), self.tag5)

class NewsTests(TestCase):
    def setUp(self):
        # Ensure tags exist before creating news
        self.tag1, _ = Tag.objects.get_or_create(name='علمی')
        self.tag2, _ = Tag.objects.get_or_create(name='فناوری')
        self.tag3, _ = Tag.objects.get_or_create(name='علوم پایه و مهندسی')
        self.tag4, _ = Tag.objects.get_or_create(name='مطالب موبایل')
        self.tag5, _ = Tag.objects.get_or_create(name='خودرو')

        # Create news instances
        self.news1 = News.objects.get_or_create(
            title='هوش مصنوعی دیپ مایند در پیشرفتی چشمگیر موفق به حل سؤالات المپیاد ریاضی شد',
            body='دیپ مایند گوگل پس از شکست‌دادن انسان‌ها در زمینه‌های مختلف از بازی گو گرفته تا بازی‌های رومیزی استراتژیک، اکنون در آستانه پیشی‌گرفتن از دانش‌آموزان برتر جهان در حل مسائل ریاضی است. این شرکت یادگیری ماشین مستقر در لندن اعلام کرده است سیستم‌ هوش مصنوعی آن‌ها چهار مسئله از شش مسئله المپیاد بین‌المللی ریاضی (IMO) سال ۲۰۲۴ را که ماه جاری در شهر باث بریتانیا به دانش‌آموزان داده شده بود، حل کرده است.',
            resources='https://www.zoomit.ir/fundamental-science/424556-alphaproof-prowess-questions-mathematical-olympiad/'
        )
        self.news1.tags.add(self.tag1, self.tag2, self.tag3)

        self.news2 = News.objects.get_or_create(
            title='ظاهراً توسعه پوکو F7 شروع شده است',
            body= 'فعلاً جزئیات زیادی از سری پوکو F7 نمی‌دانیم. احتمالاً در ماه می ۲۰۲۵ (اردیبهشت و خرداد ۱۴۰۴) باید شاهد رونمایی از میان‌رده‌های جدید پوکو باشیم. اطلاعات موجود در IMEI نشان می‌دهد که پوکو F7 پرو با شماره‌مدل 24122RKC7G احتمالاً مدل ری‌برندشده‌ی ردمی K80 با شماره‌مدل 24122RKC7C خواهد بود.',
            resources='https://www.zoomit.ir/mobile/424594-poco-starts-work-f7-series/'
        )
        self.news2.tags.add(self.tag2, self.tag4)

        self.news3 = News.objects.get_or_create(
            title='جانشین لامبورگینی اوراکان ۲۶ مرداد از راه می‌رسد',
            body= 'خودرو جدید لامبورگینی برخلاف Huracan و Gallardo، محصول کاملاً اختصاصی از این شرکت محسوب می‌شود و دیگر شباهتی به آئودی R8 نخواهد داشت. موفقیت‌های مالی اخیر لامبورگینی به آن‌ها اجازه می‌دهد بدون نیاز به تقسیم هزینه‌های توسعه با معادل R8، روی مدل کاملاً جدید تمرکز کنند.',
            resources='https://www.zoomit.ir/car/424572-lamborghini-huracan-successor/'
        )
        self.news3.tags.add(self.tag5)

    def test_news_titles(self):
        self.assertEqual(News.objects.count(), 3)
        self.assertEqual(self.news1.title, 'هوش مصنوعی دیپ مایند در پیشرفتی چشمگیر موفق به حل سؤالات المپیاد ریاضی شد')
        self.assertEqual(self.news2.title, 'ظاهراً توسعه پوکو F7 شروع شده است')
        self.assertEqual(self.news3.title, 'جانشین لامبورگینی اوراکان ۲۶ مرداد از راه می‌رسد')

    def test_news_bodies(self):
        self.assertEqual(self.news1.body,
                         'دیپ مایند گوگل پس از شکست‌دادن انسان‌ها در زمینه‌های مختلف از بازی گو گرفته تا بازی‌های رومیزی استراتژیک، اکنون در آستانه پیشی‌گرفتن از دانش‌آموزان برتر جهان در حل مسائل ریاضی است. این شرکت یادگیری ماشین مستقر در لندن اعلام کرده است سیستم‌ هوش مصنوعی آن‌ها چهار مسئله از شش مسئله المپیاد بین‌المللی ریاضی (IMO) سال ۲۰۲۴ را که ماه جاری در شهر باث بریتانیا به دانش‌آموزان داده شده بود، حل کرده است.')
        self.assertEqual(self.news2.body,
                         'فعلاً جزئیات زیادی از سری پوکو F7 نمی‌دانیم. احتمالاً در ماه می ۲۰۲۵ (اردیبهشت و خرداد ۱۴۰۴) باید شاهد رونمایی از میان‌رده‌های جدید پوکو باشیم. اطلاعات موجود در IMEI نشان می‌دهد که پوکو F7 پرو با شماره‌مدل 24122RKC7G احتمالاً مدل ری‌برندشده‌ی ردمی K80 با شماره‌مدل 24122RKC7C خواهد بود.')
        self.assertEqual(self.news3.body,
                         'خودرو جدید لامبورگینی برخلاف Huracan و Gallardo، محصول کاملاً اختصاصی از این شرکت محسوب می‌شود و دیگر شباهتی به آئودی R8 نخواهد داشت. موفقیت‌های مالی اخیر لامبورگینی به آن‌ها اجازه می‌دهد بدون نیاز به تقسیم هزینه‌های توسعه با معادل R8، روی مدل کاملاً جدید تمرکز کنند.')

    def test_news_tags(self):
        self.assertIn(self.tag1, self.news1.tags.all())
        self.assertIn(self.tag2, self.news1.tags.all())
        self.assertIn(self.tag3, self.news1.tags.all())


class NewsListAPIViewsTests(APITestCase):
    def setUp(self):
        self.tag1, _ = Tag.objects.get_or_create(name='علمی')
        self.tag2, _ = Tag.objects.get_or_create(name='فناوری')
        self.tag3, _ = Tag.objects.get_or_create(name='علوم پایه و مهندسی')

        self.news1, _ = News.objects.get_or_create(
            title='هوش مصنوعی دیپ مایند در پیشرفتی چشمگیر موفق به حل سؤالات المپیاد ریاضی شد',
            body='دیپ مایند گوگل پس از شکست‌دادن انسان‌ها در زمینه‌های مختلف از بازی گو گرفته تا بازی‌های رومیزی استراتژیک، اکنون در آستانه پیشی‌گرفتن از دانش‌آموزان برتر جهان در حل مسائل ریاضی است. این شرکت یادگیری ماشین مستقر در لندن اعلام کرده است سیستم‌ هوش مصنوعی آن‌ها چهار مسئله از شش مسئله المپیاد بین‌المللی ریاضی (IMO) سال ۲۰۲۴ را که ماه جاری در شهر باث بریتانیا به دانش‌آموزان داده شده بود، حل کرده است.',
            resources='https://www.zoomit.ir/fundamental-science/424556-alphaproof-prowess-questions-mathematical-olympiad/'
        )
        self.news1.tags.add(self.tag1, self.tag2)

        self.news2, _ = News.objects.get_or_create(
            title='ظاهراً توسعه پوکو F7 شروع شده است',
            body='فعلاً جزئیات زیادی از سری پوکو F7 نمی‌دانیم. احتمالاً در ماه می ۲۰۲۵ (اردیبهشت و خرداد ۱۴۰۴) باید شاهد رونمایی از میان‌رده‌های جدید پوکو باشیم. اطلاعات موجود در IMEI نشان می‌دهد که پوکو F7 پرو با شماره‌مدل 24122RKC7G احتمالاً مدل ری‌برندشده‌ی ردمی K80 با شماره‌مدل 24122RKC7C خواهد بود.',
            resources='https://www.zoomit.ir/mobile/424594-poco-starts-work-f7-series/'
        )
        self.news2.tags.add(self.tag2, self.tag3)

        self.news3, _ = News.objects.get_or_create(
            title='جانشین لامبورگینی اوراکان ۲۶ مرداد از راه می‌رسد',
            body='خودرو جدید لامبورگینی برخلاف Huracan و Gallardo، محصول کاملاً اختصاصی از این شرکت محسوب می‌شود و دیگر شباهتی به آئودی R8 نخواهد داشت. موفقیت‌های مالی اخیر لامبورگینی به آن‌ها اجازه می‌دهد بدون نیاز به تقسیم هزینه‌های توسعه با معادل R8، روی مدل کاملاً جدید تمرکز کنند.',
            resources='https://www.zoomit.ir/car/424572-lamborghini-huracan-successor/'
        )
        self.news3.tags.add(self.tag1, self.tag2)

    def test_get_all_news(self):
        url = '/news/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_news_by_tags(self):
        url = '/news/'
        response = self.client.get(url, {'tags': [self.tag1.name]})
        self.assertEqual(response.status_code, 200)

        news = set(News.objects.filter(tags__name__in=[self.tag1.name]))
        serializer = NewsSerializer(news, many=True)
        self.assertEqual(response.data, serializer.data)

        response = self.client.get(url, {'tags': [self.tag2.name]})
        self.assertEqual(response.status_code, 200)

        news = set(News.objects.filter(tags__name__in=[self.tag2.name]))
        serializer = NewsSerializer(news, many=True)
        self.assertEqual(response.data, serializer.data)



        response = self.client.get(url, {'tags': [self.tag1.name, self.tag3.name]})

        news = set(News.objects.filter(tags__name__in=[self.tag1.name, self.tag3.name]))
        serializer = NewsSerializer(news, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
