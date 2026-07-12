from flask import Blueprint

from controllers.dashboard_controller import dashboard_controller


# =====================================================
# DASHBOARD ROUTES
# =====================================================

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
)


# =====================================================
# DASHBOARD
# =====================================================

@dashboard_bp.route(
    "/dashboard",
    methods=["GET"],
)
def dashboard_route():
    return dashboard_controller()