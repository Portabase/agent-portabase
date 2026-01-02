import os
import logging
import requests

from celery import shared_task
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes

from core.context import AgentContext

logger = logging.getLogger("agent_logger")


@shared_task()
def send_result_backup(file_path: str, generated_id: str, status: str, method: str):
    ctx = AgentContext()
    logger.info("Sending backup result")

    try:
        edge = ctx.edge_key
        url = f"{edge.serverUrl}/api/agent/{edge.agentId}/backup"

        form_data = {
            "generatedId": (None, generated_id),
            "status": (None, status),
            "method": (None, method),
        }

        if file_path:
            server_pub = serialization.load_pem_public_key(
                edge.publicKey.encode("utf-8")
            )

            aes_key = os.urandom(32)
            iv = os.urandom(16)

            with open(file_path, "rb") as f:
                raw_data = f.read()

            padder = sym_padding.PKCS7(128).padder()
            padded = padder.update(raw_data) + padder.finalize()

            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
            encrypted = cipher.encryptor().update(padded) + cipher.encryptor().finalize()

            encrypted_key = server_pub.encrypt(
                aes_key,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            form_data["file"] = (
                f"{generated_id}.enc",
                encrypted,
                "application/octet-stream"
            )
            form_data["aes_key"] = (None, encrypted_key.hex())
            form_data["iv"] = (None, iv.hex())
        else:
            form_data["file"] = (None, "")

        response = requests.post(url, files=form_data, timeout=60)
        response.raise_for_status()

        logger.info("Backup result sent successfully")
        return {"result": True, "message": response.json()}

    except Exception as e:
        logger.exception("Backup result sending failed")
        return {"result": False, "error": str(e)}


@shared_task()
def send_result_restoration(generated_id: str, status: str):
    ctx = AgentContext()
    logger.info("Sending restoration result")

    try:
        edge = ctx.edge_key
        url = f"{edge.serverUrl}/api/agent/{edge.agentId}/restore"

        payload = {
            "generatedId": generated_id,
            "status": status,
        }

        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()

        logger.info("Restoration result sent successfully")
        return {"result": True, "message": response.json()}

    except Exception as e:
        logger.exception("Restoration result sending failed")
        return {"result": False, "error": str(e)}
