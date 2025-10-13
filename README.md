<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TOP-للشحن الإلكتروني</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/lucide/1.28.0/iconfont/lucide.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap');
        body {
            font-family: 'Tajawal', sans-serif;
        }
        .gradient-bg {
            background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%);
        }
        .product-card {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        .cart-sidebar {
            transition: transform 0.3s ease;
        }
        .star-rating {
            color: #fbbf24;
        }
    </style>
</head>
<body class="bg-gray-50">
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect } = React;

        // بيانات المنتجات
        const productsData = [
            {
                id: 1,
                name: "بطاقة جوجل بلاي 10$",
                category: "تطبيقات",
                price: 10,
                rating: 4.5,
                description: "بطاقة شحن لجوجل بلاي بقيمة 10 دولار"
            },
            {
                id: 2,
                name: "بطاقة آيتونز 25$",
                category: "تطبيقات",
                price: 25,
                rating: 4.3,
                description: "بطاقة شحن لآيتونز بقيمة 25 دولار"
            },
            {
                id: 3,
                name: "اشتراك نتفليكس 3 أشهر",
                category: "تطبيقات",
                price: 30,
                rating: 4.7,
                description: "اشتراك نتفليكس لمدة 3 أشهر"
            },
            {
                id: 4,
                name: "اشتراك سبوتيفاي 6 أشهر",
                category: "تطبيقات",
                price: 35,
                rating: 4.4,
                description: "اشتراك سبوتيفاي لمدة 6 أشهر"
            },
            {
                id: 5,
                name: "شدات ببجي 600 UC",
                category: "ألعاب",
                price: 12,
                rating: 4.8,
                description: "600 وحدة غير معروفة (UC) للعبة ببجي"
            },
            {
                id: 6,
                name: "عملات فري فاير 1000",
                category: "ألعاب",
                price: 8,
                rating: 4.2,
                description: "1000 عملة للعبة فري فاير"
            },
            {
                id: 7,
                name: "نقاط كول أوف ديوتي 2400",
                category: "ألعاب",
                price: 20,
                rating: 4.6,
                description: "2400 نقطة للعبة كول أوف ديوتي"
            },
            {
                id: 8,
                name: "بيتكوين 0.001 BTC",
                category: "عملات رقمية",
                price: 40,
                rating: 4.9,
                description: "0.001 بيتكوين للاستثمار والتداول"
            },
            {
                id: 9,
                name: "إيثيريوم 0.05 ETH",
                category: "عملات رقمية",
                price: 50,
                rating: 4.7,
                description: "0.05 إيثيريوم للاستثمار والتداول"
            }
        ];

        // مكون تصنيف النجوم
        const StarRating = ({ rating }) => {
            const fullStars = Math.floor(rating);
            const hasHalfStar = rating % 1 >= 0.5;
            
            return (
                <div className="flex items-center">
                    {[...Array(5)].map((_, i) => (
                        <span key={i} className="star-rating">
                            {i < fullStars ? 
                                <i data-lucide="star" className="w-4 h-4 fill-current"></i> : 
                                i === fullStars && hasHalfStar ? 
                                <i data-lucide="star-half" className="w-4 h-4 fill-current"></i> : 
                                <i data-lucide="star" className="w-4 h-4"></i>
                            }
                        </span>
                    ))}
                    <span className="mr-2 text-sm text-gray-600">({rating})</span>
                </div>
            );
        };

        // مكون بطاقة المنتج
        const ProductCard = ({ product, onAddToCart }) => {
            return (
                <div className="product-card bg-white rounded-xl shadow-md overflow-hidden">
                    <div className="p-6">
                        <div className="flex justify-between items-start mb-4">
                            <h3 className="text-lg font-bold text-gray-800">{product.name}</h3>
                            <span className="bg-purple-100 text-purple-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                                {product.category}
                            </span>
                        </div>
                        <p className="text-gray-600 text-sm mb-4">{product.description}</p>
                        <div className="flex justify-between items-center">
                            <div>
                                <StarRating rating={product.rating} />
                                <p className="text-xl font-bold text-purple-600 mt-2">${product.price}</p>
                            </div>
                            <button 
                                onClick={() => onAddToCart(product)}
                                className="gradient-bg text-white px-4 py-2 rounded-lg flex items-center hover:opacity-90 transition-opacity"
                            >
                                <i data-lucide="shopping-cart" className="w-4 h-4 ml-1"></i>
                                أضف للسلة
                            </button>
                        </div>
                    </div>
                </div>
            );
        };

        // مكون السلة الجانبية
        const CartSidebar = ({ isOpen, cartItems, onClose, onRemoveFromCart, onCheckout }) => {
            const totalPrice = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            
            return (
                <div className={`fixed inset-y-0 left-0 z-50 w-80 bg-white shadow-xl cart-sidebar ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
                    <div className="p-6 h-full flex flex-col">
                        <div className="flex justify-between items-center mb-6">
                            <h2 className="text-xl font-bold text-gray-800">سلة التسوق</h2>
                            <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
                                <i data-lucide="x" className="w-6 h-6"></i>
                            </button>
                        </div>
                        
                        <div className="flex-1 overflow-y-auto">
                            {cartItems.length === 0 ? (
                                <div className="text-center py-10">
                                    <i data-lucide="shopping-cart" className="w-16 h-16 text-gray-300 mx-auto mb-4"></i>
                                    <p className="text-gray-500">سلة التسوق فارغة</p>
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    {cartItems.map(item => (
                                        <div key={item.id} className="flex justify-between items-center bg-gray-50 p-3 rounded-lg">
                                            <div>
                                                <h4 className="font-medium text-gray-800">{item.name}</h4>
                                                <p className="text-sm text-gray-600">${item.price} × {item.quantity}</p>
                                            </div>
                                            <div className="flex items-center">
                                                <span className="font-bold text-purple-600 ml-2">${item.price * item.quantity}</span>
                                                <button 
                                                    onClick={() => onRemoveFromCart(item.id)}
                                                    className="text-red-500 hover:text-red-700 p-1"
                                                >
                                                    <i data-lucide="trash-2" className="w-4 h-4"></i>
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                        
                        {cartItems.length > 0 && (
                            <div className="border-t border-gray-200 pt-4 mt-4">
                                <div className="flex justify-between items-center mb-4">
                                    <span className="text-lg font-bold text-gray-800">المجموع:</span>
                                    <span className="text-xl font-bold text-purple-600">${totalPrice.toFixed(2)}</span>
                                </div>
                                <button 
                                    onClick={onCheckout}
                                    className="w-full gradient-bg text-white py-3 rounded-lg font-bold flex justify-center items-center hover:opacity-90 transition-opacity"
                                >
                                    <i data-lucide="message-circle" className="w-5 h-5 ml-2"></i>
                                    إتمام الطلب عبر واتساب
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            );
        };

        // المكون الرئيسي للتطبيق
        const App = () => {
            const [products, setProducts] = useState(productsData);
            const [cartItems, setCartItems] = useState([]);
            const [isCartOpen, setIsCartOpen] = useState(false);
            const [selectedCategory, setSelectedCategory] = useState("الكل");
            const [searchQuery, setSearchQuery] = useState("");

            // تصفية المنتجات حسب الفئة والبحث
            useEffect(() => {
                let filteredProducts = productsData;
                
                if (selectedCategory !== "الكل") {
                    filteredProducts = filteredProducts.filter(product => product.category === selectedCategory);
                }
                
                if (searchQuery) {
                    filteredProducts = filteredProducts.filter(product => 
                        product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                        product.description.toLowerCase().includes(searchQuery.toLowerCase())
                    );
                }
                
                setProducts(filteredProducts);
            }, [selectedCategory, searchQuery]);

            // إضافة منتج إلى السلة
            const addToCart = (product) => {
                setCartItems(prevItems => {
                    const existingItem = prevItems.find(item => item.id === product.id);
                    
                    if (existingItem) {
                        return prevItems.map(item => 
                            item.id === product.id 
                                ? { ...item, quantity: item.quantity + 1 } 
                                : item
                        );
                    } else {
                        return [...prevItems, { ...product, quantity: 1 }];
                    }
                });
            };

            // إزالة منتج من السلة
            const removeFromCart = (productId) => {
                setCartItems(prevItems => prevItems.filter(item => item.id !== productId));
            };

            // إرسال الطلب عبر واتساب
            const handleWhatsAppOrder = () => {
                if (cartItems.length === 0) return;
                
                const totalPrice = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
                let message = `مرحباً، أريد طلب المنتجات التالية من متجر TOP-للشحن:\n\n`;
                
                cartItems.forEach(item => {
                    message += `- ${item.name} (${item.quantity}) - $${item.price * item.quantity}\n`;
                });
                
                message += `\nالمجموع الكلي: $${totalPrice.toFixed(2)}\n\nشكراً!`;
                
                const encodedMessage = encodeURIComponent(message);
                const phoneNumber = "963964659342";
                const whatsappURL = `https://wa.me/${phoneNumber}?text=${encodedMessage}`;
                
                window.open(whatsappURL, '_blank');
            };

            // الفئات المتاحة
            const categories = ["الكل", "تطبيقات", "ألعاب", "عملات رقمية"];

            return (
                <div className="min-h-screen flex flex-col">
                    {/* الرأس */}
                    <header className="gradient-bg text-white shadow-lg">
                        <div className="container mx-auto px-4 py-4">
                            <div className="flex justify-between items-center">
                                <div className="flex items-center">
                                    <i data-lucide="zap" className="w-8 h-8 text-yellow-300"></i>
                                    <h1 className="text-2xl font-bold mr-2">TOP-للشحن</h1>
                                </div>
                                <button 
                                    onClick={() => setIsCartOpen(true)}
                                    className="relative bg-white/20 p-2 rounded-lg hover:bg-white/30 transition-colors"
                                >
                                    <i data-lucide="shopping-cart" className="w-6 h-6"></i>
                                    {cartItems.length > 0 && (
                                        <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                                            {cartItems.reduce((sum, item) => sum + item.quantity, 0)}
                                        </span>
                                    )}
                                </button>
                            </div>
                        </div>
                    </header>

                    {/* القسم الترويجي */}
                    <section className="gradient-bg text-white py-16">
                        <div className="container mx-auto px-4 text-center">
                            <h2 className="text-4xl font-bold mb-4">متجرك الموثوق للمنتجات الرقمية</h2>
                            <p className="text-xl mb-8 opacity-90">تطبيقات، ألعاب، وعملات رقمية بشحن فوري</p>
                            
                            <div className="max-w-md mx-auto">
                                <div className="relative">
                                    <input 
                                        type="text" 
                                        placeholder="ابحث عن المنتجات..." 
                                        className="w-full py-3 px-4 pr-12 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-purple-500"
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                    />
                                    <i data-lucide="search" className="w-5 h-5 text-gray-400 absolute left-4 top-3.5"></i>
                                </div>
                            </div>
                        </div>
                    </section>

                    {/* الفئات */}
                    <section className="bg-white py-8 border-b border-gray-200">
                        <div className="container mx-auto px-4">
                            <div className="flex flex-wrap justify-center gap-4">
                                {categories.map(category => (
                                    <button
                                        key={category}
                                        onClick={() => setSelectedCategory(category)}
                                        className={`px-6 py-2 rounded-full font-medium transition-colors ${
                                            selectedCategory === category 
                                            ? 'gradient-bg text-white' 
                                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                        }`}
                                    >
                                        {category}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </section>

                    {/* المنتجات */}
                    <main className="flex-1 container mx-auto px-4 py-12">
                        <h2 className="text-2xl font-bold text-gray-800 mb-8 text-center">منتجاتنا</h2>
                        
                        {products.length === 0 ? (
                            <div className="text-center py-10">
                                <i data-lucide="package" className="w-16 h-16 text-gray-300 mx-auto mb-4"></i>
                                <p className="text-gray-500">لا توجد منتجات مطابقة لبحثك</p>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {products.map(product => (
                                    <ProductCard 
                                        key={product.id} 
                                        product={product} 
                                        onAddToCart={addToCart}
                                    />
                                ))}
                            </div>
                        )}
                    </main>

                    {/* التذييل */}
                    <footer className="bg-gray-800 text-white py-12">
                        <div className="container mx-auto px-4">
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                                <div>
                                    <div className="flex items-center mb-4">
                                        <i data-lucide="zap" className="w-6 h-6 text-yellow-300"></i>
                                        <h3 className="text-xl font-bold mr-2">TOP-للشحن</h3>
                                    </div>
                                    <p className="text-gray-300">متجرك الموثوق للمنتجات الرقمية. تطبيقات، ألعاب، وعملات رقمية بشحن فوري.</p>
                                </div>
                                
                                <div>
                                    <h4 className="text-lg font-bold mb-4">الفئات</h4>
                                    <ul className="space-y-2">
                                        <li><a href="#" className="text-gray-300 hover:text-white transition-colors">التطبيقات</a></li>
                                        <li><a href="#" className="text-gray-300 hover:text-white transition-colors">الألعاب</a></li>
                                        <li><a href="#" className="text-gray-300 hover:text-white transition-colors">العملات الرقمية</a></li>
                                    </ul>
                                </div>
                                
                                <div>
                                    <h4 className="text-lg font-bold mb-4">اتصل بنا</h4>
                                    <div className="flex items-center mb-2">
                                        <i data-lucide="message-circle" className="w-5 h-5 text-green-400 ml-2"></i>
                                        <span className="text-gray-300">واتساب: 963964659342</span>
                                    </div>
                                    <p className="text-gray-300">الشحن فوري بعد تأكيد الدفع</p>
                                </div>
                            </div>
                            
                            <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
                                <p>© 2025 TOP-للشحن. جميع الحقوق محفوظة.</p>
                            </div>
                        </div>
                    </footer>

                    {/* السلة الجانبية */}
                    <CartSidebar 
                        isOpen={isCartOpen}
                        cartItems={cartItems}
                        onClose={() => setIsCartOpen(false)}
                        onRemoveFromCart={removeFromCart}
                        onCheckout={handleWhatsAppOrder}
                    />
                    
                    {/* زر فتح السلة على الهواتف */}
                    {!isCartOpen && cartItems.length > 0 && (
                        <button 
                            onClick={() => setIsCartOpen(true)}
                            className="fixed bottom-6 left-6 gradient-bg text-white p-4 rounded-full shadow-lg hover:opacity-90 transition-opacity md:hidden"
                        >
                            <i data-lucide="shopping-cart" className="w-6 h-6"></i>
                            <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                                {cartItems.reduce((sum, item) => sum + item.quantity, 0)}
                            </span>
                        </button>
                    )}
                </div>
            );
        };

        // تهيئة الأيقونات بعد التصيير
        const initLucideIcons = () => {
            if (window.lucide) {
                window.lucide.createIcons();
            }
        };

        // تصيير التطبيق
        ReactDOM.render(<App />, document.getElementById('root'));
        
        // تهيئة الأيقونات بعد تحميل الصفحة
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initLucideIcons);
        } else {
            initLucideIcons();
        }
    </script>
</body>
</html>
