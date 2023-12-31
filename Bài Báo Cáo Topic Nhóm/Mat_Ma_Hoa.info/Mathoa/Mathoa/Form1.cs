using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Security.Cryptography;
using System.IO;

namespace Mathoa
{
    public partial class Form1 : Form
    {
        string duoifile;

        public Form1()
        {
            InitializeComponent();
        }

        // mã hóa
        private static void EncryptFile(string srcFileName, string destFileName, byte[] key, byte[] iv, string thuattoan)
        {
            Stream srcFile =
                new FileStream(srcFileName, FileMode.Open, FileAccess.Read);
            Stream destFile =
                new FileStream(destFileName, FileMode.Create, FileAccess.Write);
            using (SymmetricAlgorithm alg = SymmetricAlgorithm.Create(thuattoan))
            {

                alg.Key = key;
                alg.IV = iv;

                CryptoStream cryptoStream = new CryptoStream(srcFile,
                    alg.CreateEncryptor(), CryptoStreamMode.Read);

                int bufferLength;
                byte[] buffer = new byte[1024];
                do
                {
                    bufferLength = cryptoStream.Read(buffer, 0, 1024);
                    destFile.Write(buffer, 0, bufferLength);
                } while (bufferLength > 0);


                destFile.Flush();
                Array.Clear(key, 0, key.Length);
                Array.Clear(iv, 0, iv.Length);
                cryptoStream.Clear();
                cryptoStream.Close();
                srcFile.Close();
                destFile.Close();
            }
        }


        //giải mã
        private static void DecryptFile(string srcFilename, string destfilename, byte[] key, byte[] iv, string thuattoan)
        {
            try
            {
                Stream srcfile =
                    new FileStream(srcFilename, FileMode.Open, FileAccess.Read);
                Stream destFile =
                    new FileStream(destfilename, FileMode.Create, FileAccess.Write);

                using (SymmetricAlgorithm alg = SymmetricAlgorithm.Create(thuattoan))
                {

                    alg.Key = key;
                    alg.IV = iv;
                    CryptoStream cryptoStream =new CryptoStream(destFile,alg.CreateDecryptor(),
                        CryptoStreamMode.Write);

                    int bufferLength;
                    byte[] buffer = new byte[1024];

                    do
                    {
                        bufferLength = srcfile.Read(buffer, 0, 1024);
                        cryptoStream.Write(buffer, 0, bufferLength);
                    } while (bufferLength > 0);
                    try
                    {
                        cryptoStream.FlushFinalBlock();
                        cryptoStream.Clear();
                        cryptoStream.Close();
                    }
                    catch
                    { }

                    Array.Clear(key, 0, key.Length);
                    Array.Clear(iv, 0, iv.Length);
                    srcfile.Close();
                    destFile.Close();
                }
            }
            catch
            { MessageBox.Show("Tên file đích không được trùng với file nguồn!!"); }



        }
        
        private void button1_Click_1(object sender, EventArgs e)
        {
            if (open1.ShowDialog() == DialogResult.OK)
            {
                int i;
                FileNguon.Text = open1.FileName;
                for (i = FileNguon.Text.Length - 1; i > 0; i--)
                    if (FileNguon.Text[i] == '.')
                        break;
                duoifile = FileNguon.Text.Substring(i, FileNguon.Text.Length - i);


            }
        }

        private void button2_Click_1(object sender, EventArgs e)
        {
            save1.FileName = "";
            if (save1.ShowDialog() == DialogResult.OK)
            {

                FileDich.Text = save1.FileName;
                FileDich.Text += duoifile;

            }
        }

        // thực hiện
        private void button3_Click_1(object sender, EventArgs e)
        {

            if (tx_key.Text == "")
            {
                MessageBox.Show("Chưa nhập mật khẩu!");
                return;
            }
            if (FileNguon.Text == "")
            {
                MessageBox.Show("Chọn file nguồn !");
                return;
            } if (FileDich.Text == "")
            {
                MessageBox.Show("Chọn file đích!");
                return;
            }

            byte[] key;
            byte[] iv;
            string thuattoan = kiemtraduoi(save1.FilterIndex);
            using (SymmetricAlgorithm alg = SymmetricAlgorithm.Create(thuattoan))
            {
                key = hambam(tx_key.Text, sobytekhoa(save1.FilterIndex));
                iv = new byte[8];

            }
            if (RB_mh.Checked == true)
            {
                EncryptFile(FileNguon.Text, FileDich.Text, key, iv, thuattoan);
                            Rt2.Clear();
                            Rt2.Text = "File Nguồn:" + FileNguon.Text;
                            Rt2.Text = Rt2.Text + "\n\nFile mã hóa:" + FileDich.Text;
                            Rt2.Text = Rt2.Text + " \n\nQuá trình mã hóa thành công";
               
            }
            else
            {string chuoitam;
                chuoitam=FileDich.Text;
                chuoitam = chuoitam.Substring(0, chuoitam.Length - 8);
                chuoitam = string.Concat(chuoitam, duoifile);
                DecryptFile(FileNguon.Text, chuoitam, key, iv, thuattoan);
                Rt2.Clear();
                Rt2.Text = "File Nguồn:" + FileNguon.Text;
                Rt2.Text = Rt2.Text + "\n\nFile giải mã:" + FileDich.Text;
                Rt2.Text = Rt2.Text + " \n\nQuá trình giải mã thành công";
            }
        
        }

        
        
        public static byte[] hambam(string arg, int byt)
        {
            byte[] salt = new byte[24];
            //RandomNumberGenerator.Create().GetBytes(salt);
            PasswordDeriveBytes pdb = new PasswordDeriveBytes(arg, salt);
            pdb.HashName = "SHA256"; // tên giải thuật
            pdb.IterationCount = 200;
            byte[] key = pdb.GetBytes(byt);
            return key;

        }

        public static int sobytekhoa(int thuattoan)
        {
            switch (thuattoan)
            {
                case 1: return 8;
                case 2: return 24;
                case 3: return 16;
                default: return 32;
            }

        }

        public static string kiemtraduoi(int thuattoan)
        {
            switch (thuattoan)
            {
                case 1: return "DES";
                case 2: return "3DES";
                case 3: return "RC2";
                default: return "Rijndael";
            }

        }

        private void Form1_Load(object sender, EventArgs e)
        {
            RB_mh.Checked = true;
        }

        private void btnguon_Click(object sender, EventArgs e)
        {
            if (open1.ShowDialog() == DialogResult.OK)
            {
                tx1.Text = open1.FileName;

            }
        }

        private void btkiemtra_Click(object sender, EventArgs e)
        {
            if (tx1.Text == "")
            {
                MessageBox.Show("Chưa chọn file nguồn!");
                return;
            }

            string filenguon = tx1.Text + ".txt";
            if (File.Exists(filenguon) == false)
            {
                if (MessageBox.Show("Chưa có tạo file kiểm tra!\n Bạn muốn tạo file kiểm tra liền?", "",
                    MessageBoxButtons.OKCancel, MessageBoxIcon.Question) == DialogResult.OK)
                {



                    using (HashAlgorithm hashAlg = HashAlgorithm.Create("MD5"))
                    {

                        using (Stream file = new FileStream(tx1.Text, FileMode.Open))
                        {

                            byte[] hash = hashAlg.ComputeHash(file);
                            Stream destFile =
                                new FileStream(filenguon, FileMode.Create, FileAccess.Write);
                            destFile.Write(hash, 0, 16);
                            destFile.Close();
                            Rt1.Clear();
                            Rt1.Text = "File Nguồn:" + tx1.Text;
                            Rt1.Text = Rt1.Text + "\n\nThực hiện : Tạo file kiểm tra";
                            Rt1.Text = Rt1.Text + " \n\nKết quả : HOÀN THÀNH";
                        }
                    }
                }
            }
            else
            {
                Stream srcfile =
                    new FileStream(filenguon, FileMode.Open, FileAccess.Read);
                byte[] hash = new Byte[16];
                srcfile.Read(hash, 0, 16);
                srcfile.Close();
                using (HashAlgorithm hashAlg = HashAlgorithm.Create("MD5"))
                {

                    using (Stream file = new FileStream(tx1.Text, FileMode.Open))
                    {

                        byte[] hash1 = hashAlg.ComputeHash(file);
                        if (BitConverter.ToString(hash1) == BitConverter.ToString(hash))
                        {
                            Rt1.Clear();
                            Rt1.Text = "File Nguồn: " + tx1.Text;
                            Rt1.Text = Rt1.Text + "\n\nThực hiện : Kiểm tra tính toàn vẹn của file.";
                            Rt1.Text = Rt1.Text + " \n\nKết quả : DỮ LIỆU CHƯA BỊ THAY ĐỔI !";
                        }
                        else
                        {
                            Rt1.Clear();
                            Rt1.Text = "File Nguồn: " + tx1.Text;
                            Rt1.Text = Rt1.Text + "\n\nThực hiện : Kiểm tra tính toàn vẹn của file.";
                            Rt1.Text = Rt1.Text + " \n\nKết quả : DỮ LIỆU ĐÃ BỊ THAY ĐỔI !";
                        }
                    }

                }
            }
        }


       
        public void mahoachuoi() 
            {
                    RSAParameters recipientsPublicKey;
                    CspParameters cspParams = new CspParameters();
                    cspParams.KeyContainerName = "MyKeys";
                    
                     using (RSACryptoServiceProvider rsaAlg = 
                        new RSACryptoServiceProvider(cspParams)) {
                           rsaAlg.PersistKeyInCsp = true;
                           recipientsPublicKey = rsaAlg.ExportParameters(false);
                    }
                  
                    byte[] plaintext = Encoding.Unicode.GetBytes( TxGoc.Text);
                    byte[] ciphertext = EncryptMessage(plaintext, 
                      recipientsPublicKey);
                    
                    TxDich.Text= BitConverter.ToString(ciphertext);
                    
                   }
                 
        private static byte[] EncryptMessage(byte[] plaintext, 
                    RSAParameters rsaParams) {
                    
                     byte[] ciphertext = null;
                    
                      using (RSACryptoServiceProvider rsaAlg = 
                        new RSACryptoServiceProvider()) {
                    
                        rsaAlg.ImportParameters(rsaParams);
                         ciphertext = rsaAlg.Encrypt(plaintext, true);
                    }
                    
                     Array.Clear(plaintext, 0, plaintext.Length);
                    
                    return ciphertext;
                }

        private void btmh_Click(object sender, EventArgs e)
        {
            TxDich.Clear();
            mahoachuoi();
           
        }

        private void TxGoc_TextChanged(object sender, EventArgs e)
        {
            btmh.Enabled = true;
            if (TxGoc.Text=="")
                btmh.Enabled=false;
        }

        private void btthoat_Click(object sender, EventArgs e)
        {
            this.Close();
        }
        int x, y;

        private void Pb1_MouseDown(object sender, MouseEventArgs e)
        {
            x = e.X;
            y = e.Y;
            Cursor.Current = Cursors.NoMove2D;
        }
        private void Pb1_MouseMove(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                this.Top += (e.Location.Y - y);
                this.Left += (e.Location.X - x);
            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            this.Hide();
            icon1.Visible = true;
        }

        private void icon1_MouseDoubleClick(object sender, MouseEventArgs e)
        {
            this.Show();
            icon1.Visible = false;
        }

      

    }
}