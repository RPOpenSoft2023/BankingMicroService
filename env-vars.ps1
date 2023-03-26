[System.Environment]::SetEnvironmentVariable('DATABASE_USER', 'postgres')
[System.Environment]::SetEnvironmentVariable('DATABASE_PASSWORD', 'demo')
[System.Environment]::SetEnvironmentVariable('DATABASE_NAME', 'banking-db')

[System.Environment]::SetEnvironmentVariable('USERS_MICROSERVICE_LINK', 'https://users-ms.apps.sandbox-m3.1530.p1.openshiftapps.com/user/api/verify_token')
