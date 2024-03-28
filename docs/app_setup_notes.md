# New Azure Fed Demo Setup

## Initial App Creation and Deployment

1. Create the new dev app.

    From root of the repo execute the script:

    ```powershell
    ./scripts/create_new_dev_app.ps1 -appName <appName>
    ```

2. Develop and test the app locally

3. Deploy the app to the dev environment

    ```powershell
    ./scripts/deploy_app.ps1 -appName <appName>
    ```

4. Make several changes to the container app

   - Container App | Ingress | Session Affinity
     - Enable and Save

   - Container App | Custom Domain
      - Add the custom domain (managed certificate is autocreated)
      - Setup DNS Zone as directed
      - Validate
      - Wait for binding to complete

5. Set the container app environment variables

    ```powershell
    ./scripts/set_app_env.ps1 -appName <appName>
    ```

6. Scale the app (cpu and memory are optional, defaults are 0.5 and 1.0Gi respectively)

    ```powershell
    ./scripts/set_app_scale.ps1 -appName <appName> -cpu <cpu> -memory <memory>
    ```

7. Validate the app is running at <appname>.azurefed.com

## Redploy app after development changes

1. Deploy the app to the dev environment

    ```powershell
    ./scripts/deploy_app.ps1 -appName <appName>
    ```

## Update app environment variables

1. Set the container app environment variables

    ```powershell
    ./scripts/set_app_env.ps1 -appName <appName>
    ```

## Adjust the app scale

1. Scale the app (cpu and memory are optional, defaults are 0.5 and 1.0Gi respectively)

    ```powershell
    ./scripts/set_app_scale.ps1 -appName <appName> -cpu <cpu> -memory <memory>
    ```
