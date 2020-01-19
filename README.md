# Reimplementing Asteroids

Following some of the introspection from [my blog post](https://www.brettwitty.net/implementing-asteroids.html), I thought I'd reimplement Asteroids from scratch with `pygame`. Terry Cavanagh (recently in 2020) released [the source code for VVVVV](https://github.com/TerryCavanagh/VVVVVV), warts and all. I've been encouraged to do the same.

:warning: Be warned, this is solo, hobby project, not originally intended for public consumption. The code is very rough, and the only guarantees is that it works on my machine. It is not identical to any particular historical version of Asteroids, just whatever I remembered of it from my youth.

## Getting started

These instructions will get the code onto your machine and hopefully running.

### Prerequisites

We will need Python 3.6, pygame 2.0 and numpy.

```bash
pip install --user -r requirements.txt
```

### Installing and running

Just git clone this repository into a useful place. Then

```bash
python3 asteroids.py
```

## Authors

   * [Brett Witty](https://www.brettwitty.net/)

## License

This project is licensed under the MIT License - [LICENSE.md](LICENSE.md)
