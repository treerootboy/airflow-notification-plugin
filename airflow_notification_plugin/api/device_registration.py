"""REST API for device registration."""

from flask import Blueprint, request, jsonify
from datetime import datetime
from sqlalchemy.orm import Session
from airflow.settings import Session as AirflowSession

from airflow_notification_plugin.models import DeviceRegistration, PlatformType


device_registration_blueprint = Blueprint(
    "device_registration",
    __name__,
    url_prefix="/api/v1/notification"
)


@device_registration_blueprint.route("/register-device", methods=["POST"])
def register_device():
    """
    Register or update a client device for push notifications.
    
    Expected JSON payload:
    {
        "device_token": "string",
        "platform_type": "pwa|ios|android",
        "user_id": "string"
    }
    
    Returns:
    {
        "success": true,
        "message": "Device registered successfully",
        "device_id": 123
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400
        
        device_token = data.get("device_token")
        platform_type = data.get("platform_type")
        user_id = data.get("user_id")
        
        if not all([device_token, platform_type, user_id]):
            return jsonify({
                "success": False,
                "error": "Missing required fields: device_token, platform_type, user_id"
            }), 400
        
        # Validate platform type
        try:
            platform_enum = PlatformType[platform_type.upper()]
        except KeyError:
            return jsonify({
                "success": False,
                "error": f"Invalid platform_type. Must be one of: {[p.value for p in PlatformType]}"
            }), 400
        
        # Get database session
        session = AirflowSession()
        
        try:
            # Check if device already exists
            existing_device = session.query(DeviceRegistration).filter_by(
                device_token=device_token
            ).first()
            
            if existing_device:
                # Update existing device
                existing_device.platform_type = platform_enum
                existing_device.user_id = user_id
                existing_device.is_active = True
                existing_device.last_used = datetime.utcnow()
                existing_device.updated_at = datetime.utcnow()
                session.commit()
                
                return jsonify({
                    "success": True,
                    "message": "Device updated successfully",
                    "device_id": existing_device.id
                }), 200
            else:
                # Create new device registration
                new_device = DeviceRegistration(
                    device_token=device_token,
                    platform_type=platform_enum,
                    user_id=user_id,
                    is_active=True
                )
                session.add(new_device)
                session.commit()
                
                return jsonify({
                    "success": True,
                    "message": "Device registered successfully",
                    "device_id": new_device.id
                }), 201
        
        except Exception as e:
            session.rollback()
            return jsonify({
                "success": False,
                "error": f"Database error: {str(e)}"
            }), 500
        
        finally:
            session.close()
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@device_registration_blueprint.route("/unregister-device", methods=["POST"])
def unregister_device():
    """
    Unregister a client device.
    
    Expected JSON payload:
    {
        "device_token": "string"
    }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get("device_token"):
            return jsonify({
                "success": False,
                "error": "Missing device_token"
            }), 400
        
        device_token = data.get("device_token")
        session = AirflowSession()
        
        try:
            device = session.query(DeviceRegistration).filter_by(
                device_token=device_token
            ).first()
            
            if device:
                device.is_active = False
                device.updated_at = datetime.utcnow()
                session.commit()
                
                return jsonify({
                    "success": True,
                    "message": "Device unregistered successfully"
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "error": "Device not found"
                }), 404
        
        except Exception as e:
            session.rollback()
            return jsonify({
                "success": False,
                "error": f"Database error: {str(e)}"
            }), 500
        
        finally:
            session.close()
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500
