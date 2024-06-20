<div align="center">
	<img src="https://github.com/Domejko/PyPass-Manager/assets/119700507/258bb8d7-a68d-4dac-8319-b60129d198be">
</div>

# PyPass Manager 1.1.1

**PyPass Manager** is a GUI program that allows every user to store there passwords in one place.

All the passwords are encoded with an key that's needed to decode them again. **Key should be stored on dedicated USB 
for additional security**. It's a simple way of storing passwords in one place and protecting them from accessing 
by unauthorized users.

**Notice** - Do not store sensitive information like bank account passwords, PayPal passwords or any financial accounts. 
This is only a basic protection, if something was hidden and ciphered by a human it means that it can be found and 
deciphered by human too. If Pentagon is not safe, neither are you. \
**The safest vault for your password is your memory. If that fails use notebook.**

# Prerequisites 

To install onefile-executable prebuild: 
- Windows 10 or 11
- Linux (Debian based)

To run raw python code:\
- `pip install -r requirements.txt`


# Installing PyPass Manager

Prebuild installer for each system can be found in .zip file:\

Linux (PPS Linux prebuild .deb) :\
`PyPass_manager-1.1_all.deb`

Windows (PPS Windows prebuild .exe) :\
`PyPass-Manager-Setup-1.1.1.exe`

# Running code

Tkinter is a part of python library but in some environments you may encounter `ImportError: No module named 'Tkinter'` 
solutions on this error for different environments are as follows:

💡 If you have only one version of Python installed:
- `pip install python3-tkinter`

💡 If you have Python 3 (and, possibly, other versions) installed:
- `pip3 install python3-tkinter`

💡 If you don't have PIP or it doesn't work:
- `python -m pip install python3-tkinter`
- `python3 -m pip install python3-tkinter`

💡 If you have Linux and you need to fix permissions (any one):
- `sudo pip3 install python3-tkinter`
- `pip3 install python3-tkinter --user`

💡 If you have Linux or Ubuntu with apt:
- `sudo apt-get install python3-tk`

💡 If you're using macOS and you want to install Python 3.9 Tkinter (any):
- `brew install python-tk@3.9`
- `brew install python-tk`

💡 If you have Fedora:
- `sudo dnf install python3-tkinter`

💡 If you have Windows and you have set up the py alias:
- `py -m pip install python3-tkinter`

💡 If you have Anaconda:
- `conda install -c anaconda python3-tkinter`

💡 If you have Jupyter Notebook:
- `!pip install python3-tkinter`
- `!pip3 install python3-tkinter`

# Using PyPass Manager

Start the program from an executable shortcut on desktop or from installation directory. First step is to create your 
account (top left corner) and store your Key on USB drive (you may also store it on your PC/laptop but someone may 
eventually find it and use it to decode you passwords while USB when not plugged in is inaccessible). After that you can 
log in into your account and store your first password. Everything inside is described about what function it serves 
and how to use it. You can also always delete an account that you created what is possible form your login window 
(top right corner).

# Contact

If you want to contact me you can reach me at sllawny@gmail.com.

# License

This project uses the following license: MIT License

# Update History

<table>
<thead>
	<tr>
		<th>Version</th>
		<th>Update Content</th>
	</tr>
</thead>
<tbody>
    <tr>
		<td>2024.03.23 - v1.1.1</td>
		<td>Improved hashing methods to SHA3. Fixed bug where user could not select path for his key. Fixed issue 
            where user couldn't delete his account. Refactored code and change file structure. Improved startup speed
            from executable.</td>
	</tr>
	<tr>
		<td>2023.05.19 - v1.1</td>
		<td>Improved security (changed key creation method, increased hash complexity, added sql database, improved 
            login method to mitigate brute force attacks, popup window bug fix)</td>
	</tr>
	<tr>
	    <td>2023.05.16 - v1.0</td>
	    <td>Initial version</td>
</tbody>
</table>
