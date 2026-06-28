class FormService:

    @staticmethod
    def prepare_booking(package):

        return {
            "venue_form": {
                "vendor_type": "venue",
                "vendor_name": package["venue"],
                "vendor_url": package["venue_url"],
                "event_type": "Wedding",
                
                "status": "pending_approval"
            },

            "catering_form": {
                "vendor_type": "catering",
                "vendor_name": package["caterer"],
                "vendor_url": package["caterer_url"],
                "guest_count": package["guest_count"],
               
                "status": "pending_approval"
            },

            "decorator_form": {
                "vendor_type": "decoration",
                "vendor_name": package["decorator"],
                "vendor_url": package["decorator_url"],
                
                "status": "pending_approval"
            },

            "photographer_form": {
                "vendor_type": "photography",
                "vendor_name": package["photographer"],
                "vendor_url": package["photographer_url"],
                "status": "pending_approval"
            },

            "execution_status": "READY_FOR_USER_APPROVAL"
        }
