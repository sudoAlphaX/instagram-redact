

<div align="center">
  <a href="https://github.com/sudoAlphaX/instagram-redact">  </a>

<h1 align="center">Instagram Redact</h1>

  <p align="center">
    Take back your Instagram privacy

[![Forks][forks-badge]][forks-url]
[![Stargazers][stars-badge]][stars-url]
[![Discussions][discussions-badge]][discussions-url]
[![Issues][issues-badge]][issues-url]
[![MIT License][license-badge]][license-url]

  </p>
    <p align="center">
    <a href="https://github.com/sudoAlphaX/instagram-redact"></a>
    <a href="https://github.com/sudoAlphaX/instagram-redact/issues">Report Bug</a>
    |
    <a href="https://github.com/sudoAlphaX/instagram-redact/discussions">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#inspiration">Inspiration</a></li>
        <li><a href="#built-using">Built using</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


## About The Project

Instagram Redact is used to remove your digital footprint from Instagram. This tool allows you to remove your activity from Instagram.


### Inspiration

Instagram's in-built feature to remove your digital footprint from Instagram is not good. It has a lot of rate limits and the official client doesn't allow you to perform more than 100 actions.
Hence, this tool was developed to facilitate the process of removing your activity from Instagram


### Built Using

* [![Python][python-badge]][python-url]
* [![Instagrapi][instagrapi-badge]][instagrapi-url]


## Getting Started

You can currently run this tool on your local machine.

### Prerequisites

* Python >= 3.9


### Installation

1. Clone the repo
   ```
   git clone https://github.com/sudoAlphaX/instagram-redact.git
   ```

2. Change to the directory
    ```sh
    cd instagram-redact
    ```

3. Create a Python virtual environment
    ```
    python -m venv venv
    ```

4. Activate the virtual environment
    ```sh
    venv\Scripts\activate.bat
    ```

5. Install required packages
    ```sh
    pip install -r requirements.txt
    ```


## Usage

1. Rename sampleconfig.ini to config.ini and fill in the details

2. Activate virtual environment
    ```sh
    venv\Scripts\activate.bat
    ```

3. Run main.py

* You can create a batch file to run the main.py and save it in the startup folder. Paste the following lines in the batch file:

    ```
    cd path\to\directory\instagam-redact
    venv\Scripts\python.exe main.py
    ```


## Roadmap

- [x] Unlike all liked posts
- [ ] Delete all comments
- [ ] Unlike all liked comments
- [ ] Unsend all messages in a chat
- [ ] Delete all comments on your post
- [ ] Delete all posts
  - [ ] Delete all individual type of post (Photo, Video, Reel, etc)
- [ ] Delete all highlights
- [ ] Delete all collections
- [X] Simplified Login Process
  - [ ] Multi-account support
- [ ] Uninterupted running
  - [ ] Cloud server support


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request.
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## License

Distributed under the MIT License. See `LICENSE` for more information.


## Contact

Alpha - [@sudoAlphaX](https://twitter.com/sudoAlphaX)

Repo Link: [https://github.com/sudoAlphaX/instagram-redact](https://github.com/sudoAlphaX/instagram-redact)


## Acknowledgments

* [subzeroid (Instagrapi)](https://github.com/subzeroid/instagrapi)

* [othneildrew (README Template)](https://github.com/othneildrew/Best-README-Template)

[contributors-badge]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge


<!-- MARKDOWN LINKS & IMAGES -->
[forks-badge]: https://img.shields.io/github/forks/sudoalphax/instagram-redact
[forks-url]: https://github.com/sudoalphax/instagram-redact/network/members
[stars-badge]: https://img.shields.io/github/stars/sudoalphax/instagram-redact
[stars-url]: https://github.com/sudoalphax/instagram-redact/stargazers
[issues-badge]: https://img.shields.io/github/issues/sudoalphax/instagram-redact
[issues-url]: https://github.com/sudoalphax/instagram-redact/issues
[discussions-badge]: https://img.shields.io/github/discussions/sudoalphax/instagram-redact
[discussions-url]: https://github.com/sudoalphax/instagram-redact/discussions
[python-badge]: https://img.shields.io/badge/Python-blue?logo=python&logoColor=yellow
[python-url]: https://www.python.org/
[instagrapi-badge]: https://img.shields.io/badge/Instagrapi-pink?logo=instagram
[instagrapi-url]: https://github.com/subzeroid/instagrapi
[license-badge]: https://img.shields.io/github/license/sudoalphax/instagram-redact
[license-url]: https://github.com/sudoAlphaX/instagram-redact/blob/main/LICENSE
