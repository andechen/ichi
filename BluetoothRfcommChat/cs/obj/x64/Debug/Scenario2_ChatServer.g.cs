﻿#pragma checksum "C:\Users\andec\Documents\ichi\BluetoothRfcommChat\cs\Scenario2_ChatServer.xaml" "{8829d00f-11b8-4213-878b-770e8597ac16}" "574BAB26E581431AA603171B283B30158E15FE3DF610A88B90E4958D3E5D2567"
//------------------------------------------------------------------------------
// <auto-generated>
//     This code was generated by a tool.
//
//     Changes to this file may cause incorrect behavior and will be lost if
//     the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

namespace SDKTemplate
{
    partial class Scenario2_ChatServer : 
        global::Windows.UI.Xaml.Controls.Page, 
        global::Windows.UI.Xaml.Markup.IComponentConnector,
        global::Windows.UI.Xaml.Markup.IComponentConnector2
    {
        /// <summary>
        /// Connect()
        /// </summary>
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 10.0.19041.685")]
        [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
        public void Connect(int connectionId, object target)
        {
            switch(connectionId)
            {
            case 2: // Scenario2_ChatServer.xaml line 20
                {
                    this.LayoutRoot = (global::Windows.UI.Xaml.Controls.Grid)(target);
                }
                break;
            case 3: // Scenario2_ChatServer.xaml line 25
                {
                    this.Input = (global::Windows.UI.Xaml.Controls.Grid)(target);
                }
                break;
            case 4: // Scenario2_ChatServer.xaml line 53
                {
                    this.MessageTextBox = (global::Windows.UI.Xaml.Controls.TextBox)(target);
                    ((global::Windows.UI.Xaml.Controls.TextBox)this.MessageTextBox).KeyDown += this.KeyboardKey_Pressed;
                }
                break;
            case 5: // Scenario2_ChatServer.xaml line 54
                {
                    this.SendButton = (global::Windows.UI.Xaml.Controls.Button)(target);
                    ((global::Windows.UI.Xaml.Controls.Button)this.SendButton).Click += this.SendButton_Click;
                }
                break;
            case 6: // Scenario2_ChatServer.xaml line 55
                {
                    this.ConversationListBox = (global::Windows.UI.Xaml.Controls.ListBox)(target);
                }
                break;
            case 7: // Scenario2_ChatServer.xaml line 38
                {
                    this.ListenButton = (global::Windows.UI.Xaml.Controls.Button)(target);
                    ((global::Windows.UI.Xaml.Controls.Button)this.ListenButton).Click += this.ListenButton_Click;
                }
                break;
            case 8: // Scenario2_ChatServer.xaml line 39
                {
                    this.DisconnectButton = (global::Windows.UI.Xaml.Controls.Button)(target);
                    ((global::Windows.UI.Xaml.Controls.Button)this.DisconnectButton).Click += this.DisconnectButton_Click;
                }
                break;
            case 9: // Scenario2_ChatServer.xaml line 32
                {
                    this.InputTextBlock1 = (global::Windows.UI.Xaml.Controls.TextBlock)(target);
                }
                break;
            default:
                break;
            }
            this._contentLoaded = true;
        }

        /// <summary>
        /// GetBindingConnector(int connectionId, object target)
        /// </summary>
        [global::System.CodeDom.Compiler.GeneratedCodeAttribute("Microsoft.Windows.UI.Xaml.Build.Tasks"," 10.0.19041.685")]
        [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
        public global::Windows.UI.Xaml.Markup.IComponentConnector GetBindingConnector(int connectionId, object target)
        {
            global::Windows.UI.Xaml.Markup.IComponentConnector returnValue = null;
            return returnValue;
        }
    }
}

