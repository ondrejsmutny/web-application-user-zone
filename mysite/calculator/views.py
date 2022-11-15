from django.shortcuts import render

from . import calculator_module

def calculator(request):
    error_msg = None
    result = None
    if request.method == "POST":
            try:
                float(request.POST["a"])
                float(request.POST["b"])
            except:
                error_msg = "A nebo B není číslo!"
                return render(request, "calculator/calculator.html", dict(error_msg=error_msg, result=result))

            if (float(request.POST["b"]) == 0 and request.POST["operator"] == "/"):
                    error_msg = "Chyba dělení nulou"
                    return render(request, "calculator/calculator.html", dict(error_msg=error_msg, result=result))
            if (request.POST["operator"] == "+"):
                result = calculator_module.sum(request.POST["a"], request.POST["b"])
            elif (request.POST["operator"] == "-"):
                result = calculator_module.sub(request.POST["a"], request.POST["b"])
            elif (request.POST["operator"] == "/"):
                result = calculator_module.div(request.POST["a"], request.POST["b"])
            elif (request.POST["operator"] == "*"):
                result = calculator_module.mul(request.POST["a"], request.POST["b"])
            else:
                error_msg = "Něco se pokazilo :("
                return render(request, "calculator/calculator.html", dict(error_msg=error_msg, result=result))
    return render(request, "calculator/calculator.html", dict(error_msg=error_msg, result=result))