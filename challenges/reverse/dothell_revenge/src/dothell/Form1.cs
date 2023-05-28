using System;
using System.Diagnostics;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace dothell
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void nantendoShadowBan()
        {
            try
            {
                Process[] processes = Process.GetProcesses();
                foreach (Process process in processes)
                {
                    bool flag = "dnSpy".Equals(process.ProcessName);
                    if (flag)
                    {
                        MessageBox.Show("dnSpy detected");
                        base.Close();
                    }

                    flag = "ILSpy".Equals(process.ProcessName);
                    if (flag)
                    {
                        MessageBox.Show("ILSpy detected");
                        base.Close();
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void checker_Click(object sender, EventArgs e)
        {
            /*if(true)
            {
                MessageBox.Show("Not for you!");
            }
            else
            {
                MessageBox.Show("Good password! Use this to flag.");
            }*/

            //Console.WriteLine(textBox1.Text);
            //Console.WriteLine(Form1.ActiveForm.Text)

            int c1 = 1;
            int lenPass = supplier.Text.Length;
            int lenInc1 = -1;

            while (c1 == 1)
            {
                if (lenInc1 + 5 > lenPass - 1)
                {
                    c1 = 0;
                }
                else
                {
                    lenInc1 += 5;
                    if (!supplier.Text[lenInc1].Equals(System.Text.Encoding.UTF8.GetString(System.Convert.FromBase64String("LQ=="))[0]))
                    {
                        MessageBox.Show("Not for you!");
                        return;
                    }
                }
            }

            if ((lenPass / 5) + 1 != 8)
            {
                MessageBox.Show("Not for you!");
                return;
            }

            int c2 = 1;
            int lenInc2 = 0;
            int i = 0;

            if (lenInc2 > lenPass - 1)
            {
                MessageBox.Show("Not for you!");
                return;
            }

            while (c2 == 1)
            {
                if (!supplier.Text[lenInc2].Equals(Convert.ToChar(System.Text.Encoding.UTF8.GetString(System.Convert.FromBase64String(ichi.Text))[i] - 20)))
                {
                    MessageBox.Show("Not for you!");
                    return;
                }


                if (lenInc2 + 5 > lenPass - 1)
                {
                    c2 = 0;
                }
                else
                {
                    lenInc2 += 5;
                    i += 1;
                }
            }

            int c3 = 1;
            lenInc2 = lenPass - 1;
            i = 0;

            if (lenInc2 > lenPass - 1)
            {
                MessageBox.Show("Not for you!");
                return;
            }

            while (c3 == 1)
            {
                if (!Convert.ToChar((supplier.Text[lenInc2] % 0x7F)).Equals(Convert.ToChar(System.Text.Encoding.UTF8.GetString(System.Convert.FromBase64String(ni.Text))[i] - 24)))
                {
                    MessageBox.Show("Not for you!");
                    return;
                }

                if (lenInc2 - 5 < 0)
                {
                    c3 = 0;
                }
                else
                {
                    lenInc2 -= 5;
                    i += 1;
                }
            }

            int c4 = 1;
            lenInc2 = 1;
            i = 0;

            if (lenInc2 > lenPass - 1)
            {
                MessageBox.Show("Not for you!");
                return;
            }

            while (c4 == 1)
            {
                if (!supplier.Text[lenInc2].Equals(Form1.ActiveForm.Text[i * 2]))
                {
                    MessageBox.Show("Not for you!");
                    return;
                }
                else
                {
                    if (!supplier.Text[lenInc2 + 1].Equals(Form1.ActiveForm.Text[i * 2 + 1]))
                    {
                        MessageBox.Show("Not for you!");
                        return;
                    }
                }


                if (lenInc2 + 5 > lenPass - 1)
                {
                    c4 = 0;
                }
                else
                {
                    lenInc2 += 5;
                    i += 1;
                }
            }

            MessageBox.Show("Here is your star!\nECTF{" + supplier.Text + "}", Name="Success!");
        }

        private void heyhey(object sender, EventArgs e)
        {
            nantendoShadowBan();
        }
    }
}
