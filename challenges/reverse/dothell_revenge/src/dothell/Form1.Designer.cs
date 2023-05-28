namespace dothell
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.supplier = new System.Windows.Forms.TextBox();
            this.checker = new System.Windows.Forms.Button();
            this.ichi = new System.Windows.Forms.Label();
            this.ni = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // supplier
            // 
            this.supplier.Location = new System.Drawing.Point(29, 31);
            this.supplier.Name = "supplier";
            this.supplier.Size = new System.Drawing.Size(555, 22);
            this.supplier.TabIndex = 0;
            // 
            // checker
            // 
            this.checker.Location = new System.Drawing.Point(210, 70);
            this.checker.Name = "checker";
            this.checker.Size = new System.Drawing.Size(191, 33);
            this.checker.TabIndex = 1;
            this.checker.Text = "Grab your star!";
            this.checker.UseVisualStyleBackColor = true;
            this.checker.Click += new System.EventHandler(this.checker_Click);
            // 
            // ichi
            // 
            this.ichi.AutoSize = true;
            this.ichi.BackColor = System.Drawing.Color.Transparent;
            this.ichi.Location = new System.Drawing.Point(602, 90);
            this.ichi.Name = "ichi";
            this.ichi.Size = new System.Drawing.Size(105, 16);
            this.ichi.TabIndex = 2;
            this.ichi.Text = "ZWpkaGtpYWIK";
            this.ichi.Visible = false;
            // 
            // ni
            // 
            this.ni.AutoSize = true;
            this.ni.BackColor = System.Drawing.Color.Transparent;
            this.ni.Location = new System.Drawing.Point(602, 70);
            this.ni.Name = "ni";
            this.ni.Size = new System.Drawing.Size(99, 16);
            this.ni.TabIndex = 3;
            this.ni.Text = "cnRwdnh1encK";
            this.ni.Visible = false;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(609, 115);
            this.Controls.Add(this.ni);
            this.Controls.Add(this.ichi);
            this.Controls.Add(this.checker);
            this.Controls.Add(this.supplier);
            this.Name = "Form1";
            this.Text = "Mario star grabber";
            this.Load += new System.EventHandler(this.heyhey);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox supplier;
        private System.Windows.Forms.Button checker;
        private System.Windows.Forms.Label ichi;
        private System.Windows.Forms.Label ni;
    }
}

