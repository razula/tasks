from django.shortcuts import render, HttpResponse, redirect
from .models import UserBasic, Task
from django.http import JsonResponse
from django.core import serializers
from .forms import TaskModelForm, UserBasicModelForm

####################################################################################################################################
############# General Functions ####################################################################################################
####################################################################################################################################

def home(request, message=""):
    """
    Renders the home page with user tasks and a form for adding new tasks.
    If the user is not logged in, redirects to the login page.

    Args: request (HttpRequest): The HTTP request object.
          message (str, optional): Message to display on the home page. Defaults to "".

    Returns: HttpResponse: Rendered home page.
    """
    if "username" in request.session:
        userTasks = Task.objects.filter(users__username__in=[request.session["username"]])
        message = request.GET.get('message', "")
        return render(request=request, template_name="home.html", context={"categories":userTasks.values_list("category", flat=True).distinct(), "tasks":userTasks, "addForm":TaskModelForm(), "message":message})
    else:
        return redirect("login")
    
def logout(request):
    """
    Logs out the user by removing their username from the session.

    Args: request (HttpRequest): The HTTP request object.
    Returns: HttpResponse: Redirects to the login page.
    """
    del request.session["username"]
    return redirect("login")

####################################################################################################################################
############## Users Functions #####################################################################################################
####################################################################################################################################

def loginUser(request):
    """
    Handles user login. If the request method is GET, renders the login page.
    If the request method is POST, verifies user credentials and logs them in.

    Args: request (HttpRequest): The HTTP request object.
    Returns: HttpResponse: Redirects to the home page if login is successful, otherwise redirects to the login page.
    """
    if request.method == "GET":
        return render(request=request, template_name="login.html", context={"form":UserBasicModelForm(), "users":list(UserBasic.objects.all().values_list("username", flat=True))})
    else:
        cred_list = list(request.POST.items())
        username=cred_list[0][1]
        password=cred_list[1][1]
        user = UserBasic.objects.filter(username=username, password=password)
    if user:
        request.session["username"] = username
        return redirect("home")
    else:
        return redirect("login")
    
def signup(request, method="POST"):
    """
    Handles user signup. If the request method is POST, saves the user data.

    Args: request (HttpRequest): The HTTP request object.
          method (str, optional): HTTP request method. Defaults to "POST".

    Returns: HttpResponse: Redirects to the login page after successful signup.
    """
    if request.method == "POST":
        UserBasicModelForm(request.POST).save()
        return redirect("login")
    
def deleteUsers(request):
    """
    Deletes users based on the provided user IDs.

    Args: request (HttpRequest): The HTTP request object.
    Returns: HttpResponse: Redirects to the home page after successful deletion.
    """
    for id in request.GET.getlist("id"):
        UserBasic.objects.filter(id=id).delete()
    message = "Deleted Successfully"
    return redirect(f"/?message={message}")

def usersAPI(request):
    """
    Provides an API endpoint to retrieve all users.

    Args: request (HttpRequest): The HTTP request object.
    Returns: JsonResponse: JSON response containing all users.
    """
    return JsonResponse({"allUsers":list(UserBasic.objects.all().values_list("username", flat=True)), "allUsersDict": list(UserBasic.objects.all().values())})

def sessionAPI(request):
    """
    Provides an API endpoint to retrieve the current user's session information.

    Args: request (HttpRequest): The HTTP request object.
    Returns: JsonResponse: JSON response containing the user's session information.
    """
    return JsonResponse({"userSession": request.session["username"]})

####################################################################################################################################
############# Tasks Functions ######################################################################################################
####################################################################################################################################
    
def addTask(request, method="POST"):
    """
    Adds a task to the database.

    Args: request (HttpRequest): The HTTP request object.
          method (str, optional): HTTP request method. Defaults to "POST".

    Returns: HttpResponse: Redirects to the home page after adding the task.
    """
    if request.method == "POST":
        TaskModelForm(request.POST).save()
    return redirect("home")

def deleteTask(request):
    """
    Deletes a task from the database.

    Args: request (HttpRequest): The HTTP request object.
    Returns: HttpResponse: Redirects to the home page after deleting the task.
    """
    Task.objects.filter(id=request.GET["id"]).delete()
    message = "Deleted Successfully"
    return redirect(f"/?message={message}")

def updateTask(request, method="POST"):
    """
    Updates a task in the database.

    Args: request (HttpRequest): The HTTP request object.
          method (str, optional): HTTP request method. Defaults to "POST".

    Returns: HttpResponse: Redirects to the home page after updating the task.
    """
    if request.method == "POST":
        v = list(request.POST.items())
        task = Task.objects.get(id=v[0][1])
        task.dateCreated = v[1][1]
        task.description = v[2][1]
        task.dueDate = v[3][1]
        task.notes = v[4][1]
        task.status = v[5][1]
        user=UserBasic.objects.get(username=v[6][1])
        task.users.add(user)
        task.save()
        return redirect("home")

def tasksAPI(request):
    """
    Provides an API endpoint to retrieve tasks associated with the current user.

    Args: request (HttpRequest): The HTTP request object.
    Returns: HttpResponse: JSON response containing tasks associated with the current user.
    """
    tasks = serializers.serialize('json', Task.objects.filter(users__username__in=[request.session["username"]]))
    return HttpResponse(tasks)

