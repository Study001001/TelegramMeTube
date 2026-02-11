import os
import yaml

def main():
    # Read the example config
    with open("app_bot/config-example.yml", "r") as f:
        config = yaml.safe_load(f)

    # Replace values with Environment Variables
    try:
        if "API_ID" in os.environ:
            config["telegram"]["api_id"] = int(os.environ["API_ID"])
        
        if "API_HASH" in os.environ:
            config["telegram"]["api_hash"] = os.environ["API_HASH"]
            
        if "BOT_TOKEN" in os.environ:
            config["telegram"]["token"] = os.environ["BOT_TOKEN"]
            
        if "ALLOWED_USER_IDS" in os.environ:
            # Parse comma-separated list of user IDs
            user_ids = [int(uid.strip()) for uid in os.environ["ALLOWED_USER_IDS"].split(",")]
            # Clear default allowed users and add new ones
            config["telegram"]["allowed_users"] = []
            for uid in user_ids:
                user_entry = {
                    "id": uid,
                    "is_admin": True,
                    "send_startup_message": True,
                    "download_media_type": "VIDEO",
                    "save_to_storage": False,
                    "use_url_regex_match": True,
                    "upload": {
                        "upload_video_file": True,
                        "upload_video_max_file_size": 2147483648,
                        "forward_to_group": False,
                        "forward_group_id": -00000000000,
                        "silent": False,
                        "video_caption": {
                            "include_title": True,
                            "include_filename": False,
                            "include_link": True,
                            "include_size": True
                        }
                    },
                    "save_to_database": True
                }
                config["telegram"]["allowed_users"].append(user_entry)
                
    except ValueError as e:
        print(f"Error parsing environment variables: {e}")
        exit(1)

    # Write the new config file
    with open("app_bot/config.yml", "w") as f:
        yaml.dump(config, f)
    
    print("Successfully generated app_bot/config.yml from environment variables.")

if __name__ == "__main__":
    main()
