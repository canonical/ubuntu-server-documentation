(about-web-servers)=
# About web servers

The primary function of a **web server** is to store, process and deliver **web pages** to clients. The clients communicate with the server by sending HTTP requests.

Clients, mostly via **web browsers**, request specific resources and the server responds with the content of that resource (or an error message). The response is usually a web page in the form of HTML documents -- which may include images, style sheets, scripts, and text.

## URLs

Users enter a Uniform Resource Locator (URL) to point to a web server by means of its {term}`Fully Qualified Domain Name (FQDN) <FQDN>` and a path to the required resource. For example, to view the home page of the [Ubuntu Web site](https://www.ubuntu.com) a user will enter only the FQDN:

```text
www.ubuntu.com
```

To view the [community](https://www.ubuntu.com/community) sub-page, a user will enter the FQDN followed by a path:

```text
www.ubuntu.com/community
```

## Transfer protocols

The most common protocol used to transfer web pages is the Hyper Text Transfer Protocol (HTTP). Protocols such as Hyper Text Transfer Protocol over Secure Sockets Layer (HTTPS), and File Transfer Protocol (FTP), a protocol for uploading and downloading files, are also supported.

### HTTP status codes

When accessing a web server, every HTTP request received is responded to with content and a HTTP status code. HTTP status codes are three-digit codes, which are grouped into five different classes. The class of a status code can be quickly identified by its first digit:

* **1xx** :  *Informational* - Request received, continuing process
* **2xx** :  *Success* - The action was successfully received, understood, and accepted
* **3xx** :  *Redirection* - Further action must be taken in order to complete the request
* **4xx** :  *Client Error* - The request contains bad syntax or cannot be fulfilled
* **5xx** :  *Server Error* - The server failed to fulfill an apparently valid request

For more information about status codes, [check the RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html#sec6.1.1).

## Implementation

Web servers are heavily used in the deployment of websites, and there are two different implementations:

* **Static web server**: The content of the server's response will be the hosted files "as-is".
* **Dynamic web server**:  Consists of a web server plus additional software (usually an *application server* and a *database*).

  For example, to produce the web pages you see in your web browser, the application server might fill an HTML template with contents from a database. We can therefore say that the content of the server's response is generated dynamically.
