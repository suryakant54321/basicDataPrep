Author:	Chris Holden (ceholden@gmail.com)
Date:	June 10, 2015
==============================================================================

Files
------------------------------------------------------------------------------
- Ubuntu_Mate_14.04_20150610.ova
    - md5sum: 5160e7a00826f138ae0c064073b243a0
- Ubuntu_Mate_14.04_20150727.ova
    - md5sum: 9439c77c4b7660506abace72f850193a

Details
------------------------------------------------------------------------------

This virtual machine is a VirtualBox disk image of the 14.04 LTS release of 
Ubuntu Mate distribution (https://ubuntu-mate.org/). This image is stored as
an archived Open Virtualization Format (see: 
http://en.wikipedia.org/wiki/Open_Virtualization_Format for reference).

You may load the virtual machine archive (".ova" file extension) using virtual 
machine software such as VirtualBox (https://www.virtualbox.org/) which is a 
free and open source solution for virtual machine hosting.

After downloading the virtual machine to your local computer, 
you can validate the integrity of the file transfer by computing a md5 hash and
comparing it with the uploaded hash stored in Xubuntu_14.04.md5sum. 

To load the virtual machine, you can double click on the ".ova" file to import 
the virtual machine appliance into VirtualBox. Please this instruction page for
more information on how to import the virtual appliance into VirtualBox:

http://www.virtualbox.org/manual/ch01.html#ovf

To log in, boot up the virtual machine and use the following account details:

    Username: opengeo-vm 
    Password: opengeo-vm
    
You may need to install the "Guest Additions" to access host operating system
shared folders, USB devices, and more. This process is very simple and full 
instructions are avaiable here:

https://www.virtualbox.org/manual/ch04.html
    
A number of useful related softwares are pre-installed on the machine, 
including:
    
    git
    QGIS
    Orfeo ToolBox (OTB)
    Python, including many scientific Python libraries
    R, and RStudio


LICENSE
------------------------------------------------------------------------------

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.