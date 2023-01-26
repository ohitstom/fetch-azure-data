import json
import aiohttp
import asyncio
import subprocess
import sys
import os
import psutil

from modules import globals

async def async_mass_request(json, urls, headers):
    async def request(session, url):
        async with session.get(url, headers=headers) as response:
            perms = await response.json()
            return perms

    async def get():
        async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(*[asyncio.ensure_future(request(session, url)) for url in urls])
            return results

    return await get()

async def powershell(*args, verbose=None, wait=True, cwd=None, shell="powershell", **kwargs):
    if verbose is None:
        verbose = globals.verbose

    if cwd and os.path.isdir(cwd) is False:
        cwd = None

    proc = await asyncio.create_subprocess_exec(
        shell,
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        creationflags=subprocess.CREATE_NO_WINDOW,
        **kwargs,
    )

    if wait:
        if verbose:
            # while proc.returncode is None:  # for some reason this can break...? sometimes after the process exits the loop continues and the pc fans spin up...
            while process_pid_running(proc.pid):
                line = str(await proc.stdout.readline(), encoding="utf-8")
                if line.strip() != "":
                    verbose_print(line, end="")
        else:
            await proc.wait()
    return proc

def process_pid_running(pid): # Boolean operator for running pids.
    try:
        return psutil.pid_exists(pid)
    except Exception:
        return False

def verbose_print(*args, **kwargs):
    if globals.verbose:
        print(*args, **kwargs)