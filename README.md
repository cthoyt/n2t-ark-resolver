# n2t-ark-resolver

Re-implement N2T's ARK resolver using the [`curies`](https://github.com/cthoyt/curies/) Python package.

## How to Run

Run the web app locally using:

```shell
git clone https://github.com/cthoyt/n2t-ark-resolver
cd n2t-ark-resolver
python -m pip install -r requirements.txt
python wsgi.py
```

Then, navigate to http://localhost:5000/ark:/53355/cl010277627 to get some nice art from the Louvre.
In general, you can stick any ARK after `http://localhost:5000/ark:` that is resolvable via N2T.
