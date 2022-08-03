import click
from cryptography.fernet import Fernet
import base64 
from pathlib import Path


def caesar_cipher(text: str, shift: int):
    result = ""
    for c in text:
        if (c.isupper()):
            result += chr((ord(c) + shift - 65) % 26 + 65)
        else:
            result += chr((ord(c) + shift - 65) % 26 + 65)
    return result
            
            
def build_fernet(password: str) -> Fernet:
    fullkey = ''.join(caesar_cipher(password, i) for i in range(10, 14))
    b64_key = base64.b64encode(bytes(fullkey, 'ascii'))
    f = Fernet(b64_key)
    return f


@click.group()
def cli():
    pass


@cli.command()
@click.option('--text-path', help='Path to the text file')
@click.option('--password', help='Password seen only a few frames on the video', type=click.STRING)
@click.option('--output-path', help='Path to save the encrypted text as a text file')
def decrypt(text_path: Path, password: str, output_path: Path):
    """Decrypt payload using password found in the video

    Args:
        text_path (Path): Path to the text file
        password (str): Password seen only a few frames on the video
        output_path (Path): Path to save the encrypted text as a text file
    """
    fernet = build_fernet(password)
    with open(text_path) as tf:
        ciphertext = tf.read()
    payload = bytes(ciphertext, 'ascii')
    plaintext = fernet.decrypt(payload).decode('utf')
    with open(output_path, 'w', encoding='utf-8') as of:
        of.write(plaintext)

if __name__ == "__main__":
    cli()
