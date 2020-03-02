from crm.forms import NavbarForm


def navbarform(request):


    return {
        'navbarform': NavbarForm()
    }
