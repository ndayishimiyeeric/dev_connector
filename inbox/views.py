from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message, Reply
from .forms import ConversationForm, MessageForm, ReplyForm


@login_required
def inbox(request):
    conversations = request.user.conversations.all().order_by('-updated_at')
    context = {'conversations': conversations}
    return render(request, 'inbox/inbox.html', context)


@login_required
def conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user not in conversation.participants.all():
        return redirect('inbox')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            conversation.unread.add(request.user)
            return redirect('conversation', conversation_id=conversation_id)
    else:
        form = MessageForm()

    conversation.unread.remove(request.user)
    context = {'conversation': conversation, 'form': form}
    return render(request, 'inbox/conversation.html', context)


@login_required
def new_conversation(request):
    if request.method == 'POST':
        form = ConversationForm(request.POST)
        if form.is_valid():
            conversation = form.save()
            conversation.participants.add(request.user)
            return redirect('conversation', conversation_id=conversation.id)
    else:
        form = ConversationForm()
    context = {'form': form}
    return render(request, 'inbox/new_conversation.html', context)


@login_required
def send_reply(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    conversation = message.conversation

    if request.user not in conversation.participants.all():
        return redirect('inbox')

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.message = message
            reply.save()
            conversation.unread.add(request.user)
            return redirect('conversation', conversation_id=conversation.id)
    else:
        form = ReplyForm()
    context = {'message': message, 'form': form}
    return render(request, 'inbox/send_reply.html', context)


@login_required
def toggle_star(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user not in conversation.participants.all():
        return redirect('inbox')

    if request.user in conversation.starred.all():
        conversation.starred.remove(request.user)
    else:
        conversation.starred.add(request.user)
    return redirect('inbox')


