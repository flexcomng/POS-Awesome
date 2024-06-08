import frappe
from frappe import _
from frappe.auth import LoginManager

@frappe.whitelist(allow_guest=True)
def login(usr=None, pwd=None):
    if not usr:
        return {"status": "error", "message": "'usr' parameter is required"}
    if not pwd:
        return {"status": "error", "message": "'pwd' parameter is required"}
    
    try:
        login_manager = LoginManager()
        login_manager.authenticate(usr, pwd)
        login_manager.post_login()
        authenticated_user = login_manager.user
        user = frappe.get_doc("User", authenticated_user)
        
        return {
            "status": "success",
            "sid": frappe.session.sid,
            "user": authenticated_user,
            "user_data": user.as_dict(),
        }

    except Exception as e:
        error_message = f"Login failed for user {usr}: {str(e)}"
        frappe.log_error(error_message, "Login Error")
        return {"status": "error", "message": "Invalid credentials. Please review your username and/or password"}
