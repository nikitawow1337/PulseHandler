using System;
using System.IO;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Timers;
using System.Runtime.InteropServices;

namespace HRMInterface
{

    public partial class Form1 : Form
    {
        public const int WM_NCLBUTTONDOWN = 0xA1;
        public const int HTCAPTION = 0x2;

        [DllImport("User32.dll")]
        public static extern bool ReleaseCapture();

        [DllImport("User32.dll")]
        public static extern int SendMessage(IntPtr hWnd, int Msg, int wParam, int lParam);

        private static System.Timers.Timer aTimer;
        delegate void Del(string text);

        public Form1()
        {
            InitializeComponent();

            this.BackColor = Color.Red;
            this.TransparencyKey = Color.Red;
            PictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
            Color myColor = Color.FromArgb(204, 19, 23);
            label1.BackColor = myColor;

            aTimer = new System.Timers.Timer(1000);
            aTimer.Elapsed += OnTimedEvent;
            aTimer.AutoReset = true;
            aTimer.Enabled = true;
        }

        private void PictureBox1_MouseUp(object sender, MouseEventArgs e)
        {
            using (var bmp = new Bitmap(PictureBox1.Image.Width, PictureBox1.Image.Height))
            {
                PictureBox1.DrawToBitmap(bmp, PictureBox1.ClientRectangle);
                var color = bmp.GetPixel(e.X, e.Y);
                var red = color.R;
                var green = color.G;
                var blue = color.B;
                MessageBox.Show(Convert.ToString(red + " " + green + " " + blue + ""));
            }
        }

        private void PictureBox1_MouseDown(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                ReleaseCapture();
                SendMessage(Handle, WM_NCLBUTTONDOWN, HTCAPTION, 0);
            }
        }

        private void PictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void OnTimedEvent(Object source, ElapsedEventArgs e)
        {
            string text = System.IO.File.ReadAllText("../../../../heart-rate.txt");

            label1.Invoke(new Del((s) => label1.Text = text), "newText");
            Label textLabel = new Label()
            {
                AutoSize = false,
                TextAlign = ContentAlignment.MiddleCenter,
                Dock = DockStyle.None,
                //Left = 10,
            };
            //label1.Text = text;
        }

    }
}
