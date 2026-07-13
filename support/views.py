from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from .deepseek_client import DeepSeekError, ask_deepseek

# 常见问题快捷入口
FAQ_PRESETS = [
    '如何购买火车票？',
    '如何退票？退票后余票会恢复吗？',
    '忘记密码怎么办？',
    '商务座、一等座、二等座有什么区别？',
    '未登录可以购票吗？',
]

WELCOME_MESSAGE = (
    '您好，我是 12306 智能客服小助手 🤖\n'
    '您可以咨询购票、退票、改签、登录注册等问题，我会尽快为您解答。'
)


def _now_str():
    return timezone.localtime().strftime('%H:%M')


def _get_chat_history(session):
    return session.get('chat_history', [])


def _append_message(session, role, content):
    history = _get_chat_history(session)
    history.append({
        'role': role,
        'content': content,
        'time': _now_str(),
    })
    session['chat_history'] = history[-40:]
    session.modified = True


@require_http_methods(['GET', 'POST'])
def support_view(request):
    """
    智能客服页（QQ 聊天风格）。
    对话记录保存在 session 中，刷新页面仍可查看。
    """
    if request.method == 'GET' and request.GET.get('clear') == '1':
        request.session.pop('chat_history', None)
        return render(request, 'support/faq.html', {
            'faq_presets': FAQ_PRESETS,
            'chat_history': [],
            'username': request.user.username if request.user.is_authenticated else '我',
        })

    chat_history = _get_chat_history(request.session)

    # 首次进入显示欢迎语
    if not chat_history:
        _append_message(request.session, 'bot', WELCOME_MESSAGE)
        chat_history = _get_chat_history(request.session)

    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        if not question:
            messages.warning(request, '请输入您的问题')
        else:
            _append_message(request.session, 'user', question)
            try:
                answer = ask_deepseek(question)
                _append_message(request.session, 'bot', answer)
            except DeepSeekError as exc:
                _append_message(request.session, 'bot', f'⚠️ {exc}')
                messages.error(request, str(exc))
            chat_history = _get_chat_history(request.session)

    context = {
        'faq_presets': FAQ_PRESETS,
        'chat_history': chat_history,
        'username': request.user.username if request.user.is_authenticated else '我',
    }
    return render(request, 'support/faq.html', context)
