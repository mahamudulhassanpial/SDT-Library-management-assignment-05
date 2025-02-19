from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm, UserUpdateForm, UserPasswordChangeForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views import View
from django.contrib import messages
import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from posts.models import Post, Order
from django.shortcuts import get_object_or_404



def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {
        'user' : user,
        'amount': amount,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


def send_mail_to_user(subject, template_name, context, receiver):
    mail_subject = subject
    sender_mail_message = render_to_string(template_name, context)
    mail = EmailMultiAlternatives(mail_subject, '', to=[receiver])
    mail.attach_alternative(sender_mail_message, 'text/html')
    mail.send()


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        current_datetime = datetime.datetime.now()

        messages.success(self.request, f"""Your password has been changed""")

        send_mail_to_user("You password has been changed", 'accounts/password_change_mail.html', {
            'time': current_datetime.strftime("%A, %B %d, %Y")
        }, self.request.user.email)

        return super().form_valid(form)

class UserRegistrationView(FormView):
    # template_name = 'accounts/user_registration.html'
    # form_class = UserRegistrationForm
    # success_url = reverse_lazy('profile')
    
    # def form_valid(self,form):
    #     print(form.cleaned_data)
    #     user = form.save()
    #     login(self.request, user)
    #     print(user)
    #     return super().form_valid(form) # form_valid function call hobe jodi sob thik thake

    template_name = 'accounts/user_registration_form.html'
    success_url = reverse_lazy("register")
    form_class = UserRegistrationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user=user)
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')


class UserLibraryAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        data = Post.objects.filter(author = request.user)
        orders = Order.objects.filter(user = request.user)
        return render(request, self.template_name, {'form': form , 'data': data, 'orders': orders})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        data = Post.objects.filter(author = request.user)
        orders = Order.objects.filter(user = request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form, 'data': data, 'orders': orders})
    
 # Assuming you have an Account model linked to User

def borrow_book(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user_account = request.user.account  # Assuming account balance is linked to User

    # Ensure the user has enough balance
    if user_account.balance >= post.price:
        new_balance = user_account.balance - post.price

        # Create order with new balance
        order = Order.objects.create(
            user=request.user,
            post=post,
            quantity=1,
            balance_after_borrow=new_balance
        )

        # Deduct balance
        user_account.balance = new_balance
        user_account.save()

        messages.success(request, "Book borrowed successfully!")
    else:
        messages.error(request, "Insufficient balance to borrow this book.")

    return redirect('profile')
    
