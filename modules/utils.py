import json
import aiohttp
import asyncio
<<<<<<< HEAD

def async_mass_request(json, urls, headers):
=======
import subprocess

async def async_mass_request(json, urls, headers):
>>>>>>> 5e80d19 (2:32)
    async def request(session, url):
        async with session.get(url, headers=headers) as response:
            perms = await response.json()
            return perms

    async def get():
        async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(*[asyncio.ensure_future(request(session, url)) for url in urls])
            return results

<<<<<<< HEAD
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    return asyncio.run(get())
=======
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
>>>>>>> 5e80d19 (2:32)
