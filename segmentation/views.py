from operator import attrgetter
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder

from .models import Page, Character, CharacterStatistics

from django.views import generic

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

import Image #use to cut charImg

class MyJsonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, CharacterLine):
            return {
                u'line_no': obj.line_no,
                u'left': obj.left,
                u'right': obj.right,
                u'char_lst': obj.char_lst,
            }
        if isinstance(obj, Character):
            return {
                u'id': obj.id,
                u'char': obj.char,
                u'line_no': obj.line_no,
                u'char_no': obj.char_no,
                u'top': obj.top,
                u'bottom': obj.bottom,
                u'is_correct': obj.is_correct,
            }
        return super(MyJsonEncoder, self).default(obj)

class CharacterLine:
    def __init__(self, line_no, left, right, char_lst):
        self.line_no = line_no
        self.left = left
        self.right = right
        self.char_lst = char_lst

# Create your views here.
def index(request):
    return render(request, 'segmentation/index.html')

def page_detail(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    characters = Character.objects.filter(page_id=page.id).order_by('line_no')
    temp_lst = []
    line_lst = []
    cur_line_no = 0
    for character in characters:
        character.width = character.right - character.left
        character.height = character.bottom - character.top
        if character.line_no != cur_line_no:
            if temp_lst:
                line = CharacterLine(cur_line_no, temp_lst[0].left, temp_lst[0].right, temp_lst)
                line_lst.append(line)
            cur_line_no = character.line_no
            temp_lst = [character]
        else:
            temp_lst.append(character)
    if temp_lst:
        line = CharacterLine(cur_line_no, temp_lst[0].left, temp_lst[0].right, temp_lst)
        line_lst.append(line)

    print '----------------------'
    print page
    #print line_lst
    print '----------------------'
    return render(request, 'segmentation/page_detail.html',
                  {'page': page, 'line_lst': line_lst})


class PageCheckView(generic.ListView):
    template_name = 'segmentation/page_check.html'
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Page.objects.filter(id__startswith=pk).filter(is_correct=0)[:9]

def set_page_correct(request):
    if 'id' in request.POST:
        page_id = request.POST['id']
        is_correct = int(request.POST['is_correct'])
        Page.objects.filter(id=page_id).update(is_correct=is_correct)
        data = {'status': 'ok'}
    elif 'pageArr[]' in request.POST:
        pageArr = request.POST.getlist('pageArr[]')
        Page.objects.filter(id__in = pageArr ).filter(is_correct=0).update(is_correct=1)
        data = {'status': 'ok'}
    else:
        data = {'status': 'error'}
    return JsonResponse(data)

def uploadimg(request,pk):
    def handle_uploaded_file(f):
        #PAGE_IMAGE_ROOT = '/home/share/dzj_characters/page_images/'
        destination_file = '/home/share/dzj_characters/page_images/'+pk+'.jpg'
        destination = open(destination_file, 'wb')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        Page.objects.filter(id=pk).update(is_correct=2)
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['uploadimg'])
        data = {'status': 'ok'}
        return JsonResponse(data)


def cut_char_img( page_id,char_id):
    ch = Character.objects.filter(id=char_id)
    pageimg_file = '/home/share/dzj_characters/page_images/'+page_id+'.jpg'
    charimg_file = '/home/share/dzj_characters/character_images/'+char_id+'.jpg'
    regin = (ch[0].left,ch[0].top,ch[0].right,ch[0].bottom)
    pageimg=Image.open(pageimg_file)
    cropimg = pageimg.crop(regin)
    cropimg.save(charimg_file)

def page_modify(request, page_id):
    data = {}
    if request.method == 'POST':
        for key, position in request.POST.iteritems():
            if u'-' in key:
                pos = int(float(position))
                segs = key.split(u'-')
                if len(segs) == 3:
                    typ, line_no, char_no = segs
                    line_no = int(line_no)
                    char_no = int(char_no)
                    if char_no == 0:
                        char_id = page_id + u'%02dL%02d' % (line_no, 1)
                        Character.objects.filter(id=char_id).update(top=pos,is_correct=1)
                        cut_char_img(page_id,char_id)
                    else:
                        char_id = page_id + u'%02dL%02d' % (line_no, char_no)
                        Character.objects.filter(id=char_id).update(bottom=pos,is_correct=1)
                        cut_char_img(page_id,char_id)

                        char_id = page_id + u'%02dL%02d' % (line_no, char_no + 1)
                        Character.objects.filter(id=char_id).update(top=pos,is_correct=1)
                        cut_char_img(page_id,char_id)
                else:
                    typ, line_no = segs
                    line_no = int(line_no)
                    if line_no == 0:
                        line_no = 1
                        # update right
                        Character.objects.filter(page_id=page_id, line_no=line_no).update(right=pos)
                    else:
                        # update left
                        Character.objects.filter(page_id=page_id, line_no=line_no).update(left=pos)
                        Character.objects.filter(page_id=page_id, line_no=line_no+1).update(right=pos)

        data = {'status': 'ok'}
    return JsonResponse(data)

def page_segmentation_line(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    characters = Character.objects.filter(page_id=page.id).order_by('line_no')
    temp_lst = []
    line_lst = []
    cur_line_no = 0
    for character in characters:
        character.width = character.right - character.left
        character.height = character.bottom - character.top
        if character.line_no != cur_line_no:
            if temp_lst:
                temp_lst.sort(key=attrgetter('char_no'))
                line = CharacterLine(cur_line_no, temp_lst[0].left, temp_lst[0].right, temp_lst)
                line_lst.append(line)
            cur_line_no = character.line_no
            temp_lst = [character]
        else:
            temp_lst.append(character)
    if temp_lst:
        temp_lst.sort(key=attrgetter('char_no'))
        line = CharacterLine(cur_line_no, temp_lst[0].left, temp_lst[0].right, temp_lst)
        line_lst.append(line)
    return JsonResponse(line_lst, safe=False, encoder=MyJsonEncoder)

class CharacterIndex(generic.ListView):
    model = CharacterStatistics
    template_name = 'segmentation/character_index.html'

class ErrPageIndex(generic.ListView):
    model = Character
    template_name = 'segmentation/err_page_index.html'
    def get_queryset(self):
        return Character.objects.filter(is_correct=-1).values('page').annotate(dcount=Count('page'))

def character_check(request, char):
    characters_list = Character.objects.filter(char=char).filter(is_correct=0)
    paginator = Paginator(characters_list, 3) # Show 30 characters per page
    page = request.GET.get('page')
    try:
        characters = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        characters = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        characters = paginator.page(paginator.num_pages)
    return render(request, 'segmentation/character_check.html', {'char': char, 'characters': characters})


def set_correct(request):
    if 'id' in request.POST:
        char_id = request.POST['id']
        is_correct = int(request.POST['is_correct'])
        Character.objects.filter(id=char_id).update(is_correct=is_correct)
        data = {'status': 'ok'}
    elif 'charArr[]' in request.POST:
        charArr = request.POST.getlist('charArr[]')
        Character.objects.filter(id__in = charArr ).filter(is_correct=0).update(is_correct=1)
        data = {'status': 'ok'}
    else:
        data = {'status': 'error'}
    return JsonResponse(data)

def page_image(request, page_id):
    try:
        page = Page.objects.get(id=page_id)
    except Page.DoesNotExist:
        raise Http404("Page does not exist")
    return render(request, 'segmentation/page_detail.html',
                  {'page': page})
