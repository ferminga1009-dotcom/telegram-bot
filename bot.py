
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

import requests
import json
import os
import asyncio
from datetime import datetime


# =====================================
# CONFIGURACIÓN
# =====================================

TOKEN = "8722176343:AAHWiuRnJwOCrpKn3midBCX2N6UD6L1O69s"

DECOLECTA_API_KEY = (
    "sk_15933.7C2O3tucLiYmzW8M3MDWQreknCSIATsJ"
)

ADMIN_ID = 8478153340


# =====================================
# ARCHIVO JSON
# =====================================

USUARIOS_FILE = "usuarios.json"


# =====================================
# CREAR JSON SI NO EXISTE
# =====================================

def crear_json():

    if not os.path.exists(
        USUARIOS_FILE
    ):

        with open(
            USUARIOS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {},
                f,
                indent=4,
                ensure_ascii=False
            )


crear_json()


# =====================================
# CARGAR USUARIOS
# =====================================

def cargar_usuarios():

    with open(
        USUARIOS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =====================================
# GUARDAR USUARIOS
# =====================================

def guardar_usuarios(data):

    with open(
        USUARIOS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =====================================
# VERIFICAR ADMIN
# =====================================

def es_admin(user_id):

    return user_id == ADMIN_ID


# =====================================
# VERIFICAR PREMIUM
# =====================================

def es_premium(user_id):

    usuarios = cargar_usuarios()

    user_id = str(user_id)

    if user_id not in usuarios:
        return False

    return (
        usuarios[user_id]["plan"]
        == "PREMIUM"
    )


# =====================================
# /START
# =====================================

async def start(
    update: Update,
    context:
    ContextTypes.DEFAULT_TYPE
):

    keyboard = [
        [
            InlineKeyboardButton(
                "💰 PAGO",
                callback_data="pago"
            )
        ]
    ]

    reply_markup = (
        InlineKeyboardMarkup(
            keyboard
        )
    )

    await update.message.reply_text(
        "🤖 BOT ACTIVO\n\n"
        "📌 COMANDOS:\n\n"
        "/register\n"
        "/me\n"
        "/pago\n"
        "/dni 12345678\n\n"
        "👇 Usa el botón "
        "si deseas pagar.",

        reply_markup=
        reply_markup
    )


# =====================================
# BOTÓN PAGO
# =====================================

async def button_handler(
    update: Update,
    context:
    ContextTypes.DEFAULT_TYPE
):

    query = (
        update.callback_query
    )

    await query.answer()

    if (
        query.data
        == "pago"
    ):

        try:

            with open(
                "pago.png",
                "rb"
            ) as foto:

                await (
                    query.message
                    .reply_photo(
                        photo=foto,

                        caption=
                        "💰 PAGO PREMIUM\n\n"
                        "Envía tu pago "
                        "al admin para "
                        "activar PREMIUM."
                    )
                )

        except:

            await (
                query.message
                .reply_text(
                    "❌ No encontré "
                    "pago.png"
                )
            )


# =====================================
# /REGISTER
# =====================================

async def register(
    update: Update,
    context:
    ContextTypes.DEFAULT_TYPE
):

    user = (
        update
        .effective_user
    )

    usuarios = (
        cargar_usuarios()
    )

    user_id = str(user.id)

    if user_id in usuarios:

        await (
            update.message
            .reply_text(
                "⚠️ Ya estás "
                "registrado"
            )
        )
        return

    fecha = str(
        datetime.now()
    )

    usuarios[user_id] = {

        "nombre":
        user.first_name,

        "username":
        user.username,

        "plan":
        "FREE",

        "fecha":
        fecha
    }

    guardar_usuarios(
        usuarios
    )

    await (
        update.message
        .reply_text(

            "✅ REGISTRADO\n\n"

            f"👤 Nombre: "
            f"{user.first_name}\n"

            f"🆔 Tu ID:\n"
            f"{user.id}\n\n"

            "📦 Plan:\n"
            "FREE\n\n"

            "Envía tu ID "
            "al admin "
            "para premium."
        )
    )

    try:

        username = (
            f"@{user.username}"
            if user.username
            else
            "Sin username"
        )

        await (
            context.bot
            .send_message(
                chat_id=
                ADMIN_ID,

                text=
                "🚨 NUEVO "
                "REGISTRO\n\n"

                f"👤 "
                f"{user.first_name}\n"

                f"🆔 "
                f"{user.id}\n"

                f"📛 "
                f"{username}\n\n"

                "Plan:\n"
                "FREE"
            )
        )

    except Exception as e:
        print(e)

# =====================================
# /ME
# =====================================

async def me(
    update: Update,
    context:
    ContextTypes.DEFAULT_TYPE
):

    usuarios = (
        cargar_usuarios()
    )

    user_id = str(
        update.effective_user.id
    )

    if user_id not in usuarios:

        await (
            update.message
            .reply_text(
                "❌ No estás "
                "registrado\n\n"
                "Usa /register"
            )
        )
        return

    user = usuarios[user_id]

    await (
        update.message
        .reply_text(

            "👤 TU PERFIL\n\n"

            f"🆔 ID:\n"
            f"{user_id}\n\n"

            f"👤 Nombre:\n"
            f"{user['nombre']}\n\n"

            f"📦 Plan:\n"
            f"{user['plan']}"
        )
    )


# =====================================
# /PAGO
# =====================================

async def pago(
    update: Update,
    context:
    ContextTypes.DEFAULT_TYPE
):

    try:

        with open(
            "pago.png",
            "rb"
        ) as foto:

            await (
                update.message
                .reply_photo(
                    photo=foto,

                    caption=
                    "💰 PAGO PREMIUM\n\n"
                    "Envía tu pago "
                    "al admin para "
                    "activar PREMIUM."
                )
            )

    except:

        await (
            update.message
            .reply_text(
                "❌ No encontré "
                "pago.png"
            )
        )


# =====================================
# /DNI
# =====================================

async def dni(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = (
        update.effective_user.id
    )

    # VERIFICAR PREMIUM
    if not es_premium(user_id):

        await update.message.reply_text(
            "🔒 COMANDO PREMIUM\n\n"
            "❌ No tienes acceso a /dni\n\n"
            "📦 Plan actual: FREE\n\n"
            "💰 Realiza el pago para activar PREMIUM."
        )

        try:
            with open(
                "pago.png",
                "rb"
            ) as foto:

                await update.message.reply_photo(
                    photo=foto
                )

        except:
            pass

        return

    # VALIDAR ARGUMENTO
    if not context.args:

        await update.message.reply_text(
            "Uso:\n/dni 12345678"
        )
        return

    numero = context.args[0]

    # VALIDAR DNI
    if (
        not numero.isdigit()
        or len(numero) != 8
    ):

        await update.message.reply_text(
            "❌ DNI inválido"
        )
        return

    mensaje = await (
        update.message.reply_text(
            "🔍 Consultando DNI..."
        )
    )

    try:

        url = (
            "https://api.decolecta.com/"
            f"v1/reniec/dni"
            f"?numero={numero}"
        )

        headers = {
            "Authorization":
            f"Bearer {DECOLECTA_API_KEY}"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        data = response.json()

        # DATOS
        completo = data.get(
            "full_name",
            "No encontrado"
        )

        nombres = data.get(
            "first_name",
            "No encontrado"
        )

        paterno = data.get(
            "first_last_name",
            "No encontrado"
        )

        materno = data.get(
            "second_last_name",
            "No encontrado"
        )

        # MENSAJE BONITO
        texto = f"""
🪪 CONSULTA DNI

🆔 DNI:
{numero}

👤 Nombre completo:
{completo}

📛 Nombres:
{nombres}

📌 Apellido paterno:
{paterno}

📌 Apellido materno:
{materno}
"""

        await mensaje.edit_text(
            texto
        )

    except Exception as e:

        print(e)

        await mensaje.edit_text(
            "❌ Error consultando API"
        )



# =====================================
# /USUARIOS
# SOLO ADMIN
# =====================================

async def usuarios(
    update: Update,
    context:
    ContextTypes.DEFAULT_TYPE
):

    user_id = (
        update
        .effective_user.id
    )

    if not es_admin(
        user_id
    ):

        await (
            update.message
            .reply_text(
                "❌ No eres "
                "administrador"
            )
        )
        return

    users = (
        cargar_usuarios()
    )

    if not users:

        await (
            update.message
            .reply_text(
                "No hay usuarios"
            )
        )
        return

    texto = (
        "👥 USUARIOS\n\n"
    )

    for uid, data in (
        users.items()
    ):

        texto += (
            f"🆔 {uid}\n"
            f"👤 "
            f"{data['nombre']}\n"
            f"📦 "
            f"{data['plan']}\n\n"
        )

    await (
        update.message
        .reply_text(texto)
    )

# =====================================
# /BUSCAR
# SOLO ADMIN
# =====================================

async def buscar(
    update: Update,
    context:
    ContextTypes.DEFAULT_TYPE
):

    user_id = (
        update
        .effective_user.id
    )

    if not es_admin(
        user_id
    ):

        await (
            update.message
            .reply_text(
                "❌ No eres administrador"
            )
        )
        return

    if not context.args:

        await (
            update.message
            .reply_text(
                "Uso:\n"
                "/buscar ID"
            )
        )
        return

    buscar_id = (
        context.args[0]
    )

    usuarios_data = (
        cargar_usuarios()
    )

    if (
        buscar_id
        not in usuarios_data
    ):

        await (
            update.message
            .reply_text(
                "❌ Usuario no encontrado"
            )
        )
        return

    user = (
        usuarios_data[
            buscar_id
        ]
    )

    await (
        update.message
        .reply_text(

            "🔍 USUARIO\n\n"

            f"🆔 ID:\n"
            f"{buscar_id}\n\n"

            f"👤 Nombre:\n"
            f"{user['nombre']}\n\n"

            f"📦 Plan:\n"
            f"{user['plan']}"
        )
    )


# =====================================
# /SETPREMIUM
# SOLO ADMIN
# =====================================

async def setpremium(
    update: Update,
    context:
    ContextTypes.DEFAULT_TYPE
):

    admin_id = (
        update
        .effective_user.id
    )

    if not es_admin(
        admin_id
    ):

        await (
            update.message
            .reply_text(
                "❌ No eres administrador"
            )
        )
        return

    if not context.args:

        await (
            update.message
            .reply_text(
                "Uso:\n"
                "/setpremium ID"
            )
        )
        return

    user_id = (
        context.args[0]
    )

    usuarios = (
        cargar_usuarios()
    )

    if (
        user_id
        not in usuarios
    ):

        await (
            update.message
            .reply_text(
                "❌ Usuario no encontrado"
            )
        )
        return

    usuarios[user_id][
        "plan"
    ] = "PREMIUM"

    guardar_usuarios(
        usuarios
    )

    await (
        update.message
        .reply_text(
            "✅ Usuario ahora es PREMIUM"
        )
    )

    try:

        await (
            context.bot
            .send_message(
                chat_id=
                int(user_id),

                text=
                "🎉 Tu plan "
                "ha sido activado\n\n"
                "✅ PREMIUM"
            )
        )

    except:
        pass


# =====================================
# /QUITARPREMIUM
# SOLO ADMIN
# =====================================

async def quitarpremium(
    update: Update,
    context:
    ContextTypes.DEFAULT_TYPE
):

    admin_id = (
        update
        .effective_user.id
    )

    if not es_admin(
        admin_id
    ):

        await (
            update.message
            .reply_text(
                "❌ No eres administrador"
            )
        )
        return

    if not context.args:

        await (
            update.message
            .reply_text(
                "Uso:\n"
                "/quitarpremium ID"
            )
        )
        return

    user_id = (
        context.args[0]
    )

    usuarios = (
        cargar_usuarios()
    )

    if (
        user_id
        not in usuarios
    ):

        await (
            update.message
            .reply_text(
                "❌ Usuario no encontrado"
            )
        )
        return

    usuarios[user_id][
        "plan"
    ] = "FREE"

    guardar_usuarios(
        usuarios
    )

    await (
        update.message
        .reply_text(
            "❌ Premium eliminado"
        )
    )


# =====================================
# /ADMIN
# =====================================

async def admin(
    update: Update,
    context:
    ContextTypes.DEFAULT_TYPE
):

    user_id = (
        update
        .effective_user.id
    )

    if not es_admin(
        user_id
    ):

        await (
            update.message
            .reply_text(
                "❌ No eres administrador"
            )
        )
        return

    await (
        update.message
        .reply_text(

            "👑 PANEL ADMIN\n\n"

            "/usuarios\n"
            "/buscar ID\n"
            "/setpremium ID\n"
            "/quitarpremium ID"
        )
    )


# =====================================
# MAIN
# =====================================

def main():

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "register",
            register
        )
    )

    app.add_handler(
        CommandHandler(
            "me",
            me
        )
    )

    app.add_handler(
        CommandHandler(
            "pago",
            pago
        )
    )

    app.add_handler(
        CommandHandler(
            "dni",
            dni
        )
    )

    app.add_handler(
        CommandHandler(
            "usuarios",
            usuarios
        )
    )

    app.add_handler(
        CommandHandler(
            "buscar",
            buscar
        )
    )

    app.add_handler(
        CommandHandler(
            "setpremium",
            setpremium
        )
    )

    app.add_handler(
        CommandHandler(
            "quitarpremium",
            quitarpremium
        )
    )

    app.add_handler(
        CommandHandler(
            "admin",
            admin
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    print(
        "🚀 BOT ENCENDIDO"
    )

    app.run_polling(
        drop_pending_updates=True,
        poll_interval=0.2
    )


if __name__ == "__main__":

    asyncio.set_event_loop(
        asyncio.new_event_loop()
    )

    main()





