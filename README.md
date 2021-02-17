[![Gitter Chat](https://img.shields.io/badge/gitter-join%20chat-brightgreen.svg)](https://gitter.im/CiscoSecurity/Threat-Response "Gitter Chat")
# Shodan Relay (Cisco Hosted)

A Cisco SecureX Concrete Relay implementation using 
[Shodan](https://www.shodan.io/)
as a third-party Cyber Threat Intelligence service provider.

The Relay itself is just a simple application written in Python that can be easily packaged and deployed.  This relay is now Cisco Hosted and no longer requires AWS Lambda.

The code is provided here purely for educational purposes.

## Rationale

- We need an application that will translate API requests from SecureX Threat Response to the third-party integration, and vice versa.
- We need an application that can be completely self contained within a virtualized container using Docker.

## Testing (Optional)

If you want to test the application you will require Docker and several dependencies from the [requirements.txt](code/requirements.txt) file:
```
pip install --upgrade --requirement code/requirements.txt
```

You can perform two kinds of testing:

- Run static code analysis checking for any semantic discrepancies and [PEP 8](https://www.python.org/dev/peps/pep-0008/) compliance:

  `flake8 code`

- Run the suite of unit tests and measure the code coverage:
  `cd code`
  `coverage run --source api/ -m pytest --verbose tests/unit/ && coverage report`

**NOTE.** If you need input data for testing purposes you can use data from the
[observables.json](code/observables.json) file.

### Building the Docker Container
In order to build the application, we need to use a `Dockerfile`.  

 1. Open a terminal.  Build the container image using the `docker build` command.

```
docker build -t tr-05-shodan .
```

 2. Once the container is built, and an image is successfully created, start your container using the `docker run` command and specify the name of the image we have just created.  By default, the container will listen for HTTP requests using port 9090.

```
docker run -dp 9090:9090 --name tr-05-shodan tr-05-shodan
```

 3. Watch the container logs to ensure it starts correctly.

```
docker logs tr-05-shodan
```

 4. Once the container has started correctly, open your web browser to http://localhost:9090.  You should see a response from the container.

```
curl http://localhost:9090
```

## Implementation Details

### Implemented Relay Endpoints

- `POST /health`
  - Checks if the service is available at the moment.

- `POST /refer/observables`
  - Accepts a list of observables and filters out unsupported ones.
  - Builds a search link per each supported observable to pivot back to the
  underlying external service and look up the observable there.
  - Builds a browse link per each supported observable to pivot back
  directly to the observable page.
  - Returns a list of those links.
  
- `POST /version`
  - Returns the current version of the application.

### Supported Types of Observables

- `ip`
- `domain`
