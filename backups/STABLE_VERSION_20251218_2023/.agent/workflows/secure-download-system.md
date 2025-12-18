# 🔒 SISTEM SECURIZAT DE DOWNLOAD & VÂNZĂRI

## Arhitectură Completă pentru Protecție Produse Digitale

---

## 🎯 OBIECTIV

Crearea unui sistem ultra-securizat pentru vânzarea și distribuirea produselor digitale care previne:
- ❌ Pirateria și distribuirea neautorizată
- ❌ Download-uri multiple cu o singură achiziție
- ❌ Partajarea link-urilor de download
- ❌ Accesul neautorizat la fișiere

---

## 🏗️ ARHITECTURĂ SISTEM

### **Componente Principale:**

```
┌─────────────────────────────────────────────────────┐
│                  FRONTEND (Public)                   │
│  - Product Pages                                     │
│  - Shopping Cart                                     │
│  - Checkout                                          │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              PAYMENT GATEWAY                         │
│  - Stripe / PayPal                                   │
│  - Payment Verification                              │
│  - Webhook Handling                                  │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│                BACKEND API (Secure)                  │
│  - Order Processing                                  │
│  - License Generation                                │
│  - Token Creation                                    │
│  - Download Link Generation                          │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              SECURE FILE STORAGE                     │
│  - AWS S3 (Private Buckets)                          │
│  - Cloudflare R2                                     │
│  - Digital Ocean Spaces                              │
│  - Encrypted Files                                   │
└─────────────────────────────────────────────────────┘
```

---

## 🔐 METODE DE SECURIZARE

### **1. TOKEN-BASED DOWNLOAD SYSTEM**

#### **Cum Funcționează:**

1. **Utilizatorul cumpără produsul** → Payment processed
2. **Backend generează token unic** → Expirare 24 ore
3. **Email cu link securizat** → `https://kidsdigitalhub.com/download?token=ABC123XYZ`
4. **Validare token** → Verifică: valid, neexpirat, nefolosit
5. **Download unic** → Token invalidat după download
6. **Fișier șters** → Link expiră permanent

#### **Implementare:**

```javascript
// Backend (Node.js + Express)
const crypto = require('crypto');
const jwt = require('jsonwebtoken');

// Generate secure download token
function generateDownloadToken(orderId, productId, userId) {
  const payload = {
    orderId: orderId,
    productId: productId,
    userId: userId,
    timestamp: Date.now(),
    nonce: crypto.randomBytes(16).toString('hex')
  };
  
  // JWT token cu expirare 24 ore
  const token = jwt.sign(payload, process.env.JWT_SECRET, {
    expiresIn: '24h'
  });
  
  return token;
}

// Validate and process download
app.get('/api/download', async (req, res) => {
  try {
    const { token } = req.query;
    
    // 1. Verify JWT token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // 2. Check if token already used
    const isUsed = await checkTokenUsed(token);
    if (isUsed) {
      return res.status(403).json({ error: 'Token already used' });
    }
    
    // 3. Verify order and payment
    const order = await Order.findById(decoded.orderId);
    if (!order || order.status !== 'paid') {
      return res.status(403).json({ error: 'Invalid order' });
    }
    
    // 4. Generate temporary signed URL (expires in 5 minutes)
    const signedUrl = await generateSignedUrl(decoded.productId, 300);
    
    // 5. Mark token as used
    await markTokenAsUsed(token);
    
    // 6. Log download
    await logDownload(decoded.userId, decoded.productId, req.ip);
    
    // 7. Redirect to signed URL
    res.redirect(signedUrl);
    
  } catch (error) {
    res.status(403).json({ error: 'Invalid or expired token' });
  }
});
```

---

### **2. SIGNED URLs (AWS S3 / Cloudflare R2)**

#### **Avantaje:**
- ✅ URL-uri temporare (5-15 minute)
- ✅ Nu pot fi partajate (expiră rapid)
- ✅ Verificare automată de către cloud provider

#### **Implementare AWS S3:**

```javascript
const AWS = require('aws-sdk');
const s3 = new AWS.S3({
  accessKeyId: process.env.AWS_ACCESS_KEY,
  secretAccessKey: process.env.AWS_SECRET_KEY,
  region: 'us-east-1'
});

async function generateSignedUrl(productId, expiresIn = 300) {
  const fileName = `products/${productId}.zip`;
  
  const params = {
    Bucket: 'kidsdigitalhub-products-private',
    Key: fileName,
    Expires: expiresIn, // 5 minutes
    ResponseContentDisposition: `attachment; filename="${productId}.zip"`
  };
  
  const signedUrl = await s3.getSignedUrlPromise('getObject', params);
  return signedUrl;
}
```

---

### **3. WATERMARKING & FINGERPRINTING**

#### **Pentru Imagini/PDFs:**

```javascript
const PDFDocument = require('pdfkit');
const sharp = require('sharp');

// Add watermark to PDF
async function watermarkPDF(pdfPath, userId, orderId) {
  const doc = new PDFDocument();
  
  // Add invisible watermark
  doc.fontSize(8)
     .fillColor('#FFFFFF', 0.01) // Almost invisible
     .text(`User: ${userId} | Order: ${orderId}`, 10, 10);
  
  // Add visible watermark
  doc.fontSize(40)
     .fillColor('#000000', 0.1)
     .rotate(-45)
     .text('Licensed to: ' + userId, 200, 400);
  
  return doc;
}

// Add watermark to image
async function watermarkImage(imagePath, userId) {
  const watermarkText = `© Kids Digital Hub - Licensed to User ${userId}`;
  
  await sharp(imagePath)
    .composite([{
      input: Buffer.from(
        `<svg><text x="10" y="20" font-size="12" fill="rgba(255,255,255,0.5)">${watermarkText}</text></svg>`
      ),
      gravity: 'southeast'
    }])
    .toFile('watermarked-' + imagePath);
}
```

---

### **4. LICENSE KEY SYSTEM**

#### **Pentru Produse Interactive (Apps, Games):**

```javascript
// Generate unique license key
function generateLicenseKey(userId, productId) {
  const data = `${userId}-${productId}-${Date.now()}`;
  const hash = crypto.createHash('sha256').update(data).digest('hex');
  
  // Format: XXXX-XXXX-XXXX-XXXX
  const key = hash.substring(0, 16).toUpperCase()
    .match(/.{1,4}/g)
    .join('-');
  
  return key;
}

// Validate license key
async function validateLicense(licenseKey, productId) {
  const license = await License.findOne({ 
    key: licenseKey, 
    productId: productId 
  });
  
  if (!license) return false;
  if (license.revoked) return false;
  if (license.activations >= license.maxActivations) return false;
  
  // Increment activation count
  license.activations += 1;
  await license.save();
  
  return true;
}
```

---

### **5. DEVICE FINGERPRINTING**

#### **Limitare Download pe Device:**

```javascript
const Fingerprint2 = require('fingerprintjs2');

// Client-side: Generate device fingerprint
async function getDeviceFingerprint() {
  const components = await Fingerprint2.getPromise();
  const values = components.map(c => c.value);
  const fingerprint = Fingerprint2.x64hash128(values.join(''), 31);
  return fingerprint;
}

// Server-side: Validate device
app.post('/api/validate-device', async (req, res) => {
  const { token, fingerprint } = req.body;
  
  const download = await Download.findOne({ token });
  
  if (download.deviceFingerprint && 
      download.deviceFingerprint !== fingerprint) {
    return res.status(403).json({ 
      error: 'This download link is tied to another device' 
    });
  }
  
  // Save fingerprint on first download
  if (!download.deviceFingerprint) {
    download.deviceFingerprint = fingerprint;
    await download.save();
  }
  
  res.json({ valid: true });
});
```

---

### **6. RATE LIMITING & ABUSE PREVENTION**

```javascript
const rateLimit = require('express-rate-limit');

// Limit download attempts
const downloadLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 3, // Max 3 downloads per IP
  message: 'Too many download attempts. Please try again later.'
});

app.get('/api/download', downloadLimiter, async (req, res) => {
  // Download logic
});

// Monitor suspicious activity
async function detectAbusePatterns(userId) {
  const recentDownloads = await Download.find({
    userId: userId,
    createdAt: { $gte: new Date(Date.now() - 3600000) } // Last hour
  });
  
  if (recentDownloads.length > 10) {
    // Flag account for review
    await flagAccount(userId, 'Excessive downloads');
    return true;
  }
  
  return false;
}
```

---

## 📧 EMAIL DELIVERY SYSTEM

### **Secure Download Email Template:**

```javascript
const nodemailer = require('nodemailer');

async function sendDownloadEmail(order) {
  const downloadToken = generateDownloadToken(
    order._id, 
    order.productId, 
    order.userId
  );
  
  const downloadUrl = `https://kidsdigitalhub.com/download?token=${downloadToken}`;
  
  const emailHTML = `
    <h2>Thank you for your purchase! 🎉</h2>
    <p>Your order #${order._id} has been confirmed.</p>
    
    <div style="background: #f0f0f0; padding: 20px; border-radius: 10px;">
      <h3>Download Your Product:</h3>
      <p><strong>Product:</strong> ${order.productName}</p>
      <p><strong>Download Link (valid for 24 hours):</strong></p>
      <a href="${downloadUrl}" 
         style="display: inline-block; background: #FF6B9D; color: white; 
                padding: 15px 30px; text-decoration: none; border-radius: 5px;">
        Download Now
      </a>
    </div>
    
    <p><strong>Important:</strong></p>
    <ul>
      <li>This link expires in 24 hours</li>
      <li>You can download the product once</li>
      <li>Do not share this link</li>
      <li>Save the file immediately after download</li>
    </ul>
    
    <p>Need help? Contact us at support@kidsdigitalhub.com</p>
  `;
  
  await transporter.sendMail({
    from: 'Kids Digital Hub <noreply@kidsdigitalhub.com>',
    to: order.userEmail,
    subject: `Your Download Link - Order #${order._id}`,
    html: emailHTML
  });
}
```

---

## 💾 DATABASE SCHEMA

### **Orders Table:**

```javascript
const OrderSchema = new mongoose.Schema({
  orderId: { type: String, unique: true, required: true },
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  productId: { type: mongoose.Schema.Types.ObjectId, ref: 'Product' },
  amount: { type: Number, required: true },
  currency: { type: String, default: 'USD' },
  status: { 
    type: String, 
    enum: ['pending', 'paid', 'failed', 'refunded'],
    default: 'pending'
  },
  paymentMethod: String,
  paymentId: String, // Stripe payment intent ID
  downloadToken: String,
  downloadCount: { type: Number, default: 0 },
  maxDownloads: { type: Number, default: 1 },
  tokenExpiry: Date,
  deviceFingerprint: String,
  ipAddress: String,
  createdAt: { type: Date, default: Date.now },
  downloadedAt: Date
});
```

### **Downloads Log:**

```javascript
const DownloadLogSchema = new mongoose.Schema({
  orderId: { type: mongoose.Schema.Types.ObjectId, ref: 'Order' },
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  productId: { type: mongoose.Schema.Types.ObjectId, ref: 'Product' },
  ipAddress: String,
  userAgent: String,
  deviceFingerprint: String,
  downloadedAt: { type: Date, default: Date.now },
  fileSize: Number,
  success: Boolean
});
```

---

## 🔒 BEST PRACTICES

### **1. Encryption at Rest:**
```bash
# Encrypt files before upload to S3
openssl enc -aes-256-cbc -salt -in product.zip -out product.zip.enc -k YOUR_SECRET_KEY
```

### **2. HTTPS Only:**
- Force SSL/TLS pentru toate conexiunile
- HSTS headers
- Certificate pinning

### **3. Environment Variables:**
```env
# .env file (NEVER commit to Git!)
JWT_SECRET=super_secret_random_string_here
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
STRIPE_SECRET_KEY=sk_live_...
DATABASE_URL=mongodb://...
ENCRYPTION_KEY=your_encryption_key
```

### **4. Monitoring & Alerts:**
```javascript
// Alert on suspicious activity
async function monitorDownloads() {
  const suspiciousDownloads = await Download.aggregate([
    {
      $match: {
        createdAt: { $gte: new Date(Date.now() - 3600000) }
      }
    },
    {
      $group: {
        _id: '$ipAddress',
        count: { $sum: 1 }
      }
    },
    {
      $match: { count: { $gt: 5 } }
    }
  ]);
  
  if (suspiciousDownloads.length > 0) {
    await sendAlertEmail('Suspicious download activity detected');
  }
}
```

---

## 📊 IMPLEMENTATION ROADMAP

### **Phase 1: Basic Security (Week 1-2)**
- [x] Token-based download system
- [x] Email delivery
- [x] Single-use links
- [x] 24-hour expiration

### **Phase 2: Advanced Security (Week 3-4)**
- [ ] Signed URLs (AWS S3)
- [ ] Device fingerprinting
- [ ] Rate limiting
- [ ] Abuse detection

### **Phase 3: Premium Features (Week 5-6)**
- [ ] Watermarking
- [ ] License key system
- [ ] Multi-device support (Premium tier)
- [ ] Download manager

### **Phase 4: Analytics & Optimization (Week 7-8)**
- [ ] Download analytics
- [ ] Conversion tracking
- [ ] A/B testing
- [ ] Performance optimization

---

## 💰 COST ESTIMATION

### **Infrastructure:**
- **AWS S3:** ~$0.023/GB storage + $0.09/GB transfer = ~$50-100/month
- **Cloudflare R2:** $0.015/GB storage (no egress fees) = ~$30-50/month
- **Database (MongoDB Atlas):** $57/month (M10 cluster)
- **Email (SendGrid):** Free tier (100 emails/day) or $15/month
- **SSL Certificate:** Free (Let's Encrypt)

**Total:** ~$100-200/month pentru început

---

## ✅ CHECKLIST FINAL

- [ ] Backend API setup (Node.js + Express)
- [ ] Database schema (MongoDB)
- [ ] Payment integration (Stripe)
- [ ] Token generation system
- [ ] Email delivery (SendGrid/Mailgun)
- [ ] File storage (AWS S3 / Cloudflare R2)
- [ ] Signed URLs implementation
- [ ] Rate limiting
- [ ] Logging & monitoring
- [ ] Testing (unit + integration)
- [ ] Security audit
- [ ] Documentation

---

**Acest sistem oferă protecție maximă împotriva piraterie și asigură că fiecare vânzare este legitimă și securizată! 🔒**
