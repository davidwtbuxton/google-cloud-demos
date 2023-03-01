Using Secret Manager for database passwords
===========================================

https://cloud.google.com/secret-manager/

Extend django-environ to read environment variables stored in Google Secret Manager.

Create a secret named "app_environ". Set the value to [env-name]=[value] pairs, one per line.


    cat <<- EOF > secrets.txt
    DATABASE_URL=psql://postgres:secret@localhost:5432/my-database
    DEBUG=0
    SECRET_KEY=xyz
    EOF
    gcloud secrets create app_environ --data-file secrets.txt

Like django-environ, use an instance of `cloudsecrets.Env` to assign values in your project's settings module:

    import secretmanagerenv

    env = secretmanagerenv.Env(name="app_environ", version=1)
    DEBUG = env.bool("DEBUG")
    DATABASES = {"default": env.db_url("DATABASE_URL")}
    SECRET_KEY = env.str("SECRET_KEY")
