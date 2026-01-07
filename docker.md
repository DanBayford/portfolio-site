# dev

# prod

## Rebuild a given service

`docker-compose -f compose.prod.yml build web`

## Start/restart a given service (detached)

`docker-compose -f compose.prod.yml up -d web`

## Build and dstart a given service (detached)

`docker-compose -f compose.prod.yml up -d --build`

## Examples of executing Python commands in a running service

`docker-compose -f compose.prod.yml exec web python manage.py migrate --noinput`
`docker-compose -f compose.prod.yml exec web python manage.py collectstatic --no-input --clear`

## Bring down a set of services (inc volumnes!)

`docker-compose -f compose.prod.yml down -v`
